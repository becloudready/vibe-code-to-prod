#!/usr/bin/env python3
"""
cleanup-student-resources.py

Finds and deletes all AWS resources created by students during labs.
All student resources use the "student-" prefix enforced by IAM policies.

Usage:
    # Dry run — preview everything (safe, no deletions)
    python cleanup-student-resources.py --region us-east-1

    # Delete all student resources
    python cleanup-student-resources.py --region us-east-1 --delete

    # Delete one student only
    python cleanup-student-resources.py --region us-east-1 --delete --student john.doe

    # Delete only users listed in a file (one username per line, or a CSV with 'username' column)
    python cleanup-student-resources.py --region us-east-1 --delete --users-file students.csv
"""

import boto3
import argparse
import csv
import os
import sys
from botocore.exceptions import ClientError

# ─── CLI ─────────────────────────────────────────────────────────────────────

parser = argparse.ArgumentParser(description="Clean up student AWS resources")
parser.add_argument("--region",     required=True, help="AWS region (e.g. us-east-1)")
parser.add_argument("--delete",     action="store_true", help="Actually delete resources (default is dry run)")
parser.add_argument("--student",    default=None, help="Target a single student by username (e.g. john.doe)")
parser.add_argument("--users-file", default=None, help="Path to a CSV or .txt file with usernames to delete")
parser.add_argument("--profile",    default=None, help="AWS CLI profile to use")
args = parser.parse_args()

DRY_RUN = not args.delete
REGION  = args.region

# ─── Build target user list ───────────────────────────────────────────────────

TARGET_USERS = None  # None means "match all student-* by prefix"

if args.users_file:
    if not os.path.exists(args.users_file):
        print(f"ERROR: --users-file '{args.users_file}' not found.")
        sys.exit(1)

    TARGET_USERS = []
    with open(args.users_file, newline="") as f:
        # Auto-detect CSV vs plain text
        sample = f.read(1024)
        f.seek(0)
        if "," in sample:
            reader = csv.DictReader(f)
            # Accept 'username' or 'full_name' column
            col = next((c for c in reader.fieldnames if c.lower() in ("username", "user_name")), None)
            if not col:
                print(f"ERROR: CSV must have a 'username' column. Found: {reader.fieldnames}")
                sys.exit(1)
            TARGET_USERS = [row[col].strip() for row in reader if row[col].strip()]
        else:
            KNOWN_HEADERS = {"username", "user_name", "name"}
            lines = [line.strip() for line in f if line.strip()]
            # Skip header line if present
            if lines and lines[0].lower() in KNOWN_HEADERS:
                lines = lines[1:]
            TARGET_USERS = list(dict.fromkeys(lines))  # deduplicate, preserve order

    print(f"Loaded {len(TARGET_USERS)} user(s) from {args.users_file}")

elif args.student:
    TARGET_USERS = [args.student]

# ─── Helper: should this resource name be included? ──────────────────────────

PREFIX = "student-"

def is_targeted(resource_name):
    """Return True if the AWS resource (Lambda, S3, EC2...) belongs to a targeted student.
    These resources are named student-<username>-... by convention."""
    if not resource_name.startswith(PREFIX):
        return False
    if TARGET_USERS is None:
        return True  # match all student-* resources
    suffix = resource_name[len(PREFIX):]  # e.g. "john.doe-task-tracker-abc123"
    return any(suffix.startswith(u) for u in TARGET_USERS)

def is_iam_user_targeted(username):
    """Return True if the IAM username itself is in the target list.
    IAM usernames are plain (e.g. john.doe), not prefixed with student-."""
    if TARGET_USERS is None:
        return True  # no filter — delete all
    return username in TARGET_USERS

# ─────────────────────────────────────────────────────────────────────────────

session = boto3.Session(profile_name=args.profile, region_name=REGION)

# ─── Validate credentials before doing any work ───────────────────────────────
try:
    session.client("sts").get_caller_identity()
except ClientError as e:
    code = e.response["Error"]["Code"]
    if code in ("InvalidClientTokenId", "ExpiredTokenException"):
        print("\n[FATAL] AWS credentials are invalid or expired.")
        print("  Run: aws sso login  (or re-export your credentials)")
        sys.exit(1)
    raise

label = "all student-* resources" if TARGET_USERS is None else f"{len(TARGET_USERS)} user(s)"
print(f"\n{'[DRY RUN] ' if DRY_RUN else '[DELETING] '}Target: {label}")
print(f"Region: {REGION}\n")

deleted = []
errors  = []

def log(resource_type, name, action="would delete"):
    label = action if DRY_RUN else "deleted"
    print(f"  {'[DRY RUN]' if DRY_RUN else '[DELETED]'} {resource_type}: {name}")

EXPIRED_TOKEN_CODES = {"InvalidClientTokenId", "ExpiredTokenException", "RequestExpired"}

def record_error(resource_type, name, e):
    code = e.response["Error"]["Code"] if hasattr(e, "response") else ""
    if code in EXPIRED_TOKEN_CODES:
        print(f"\n[FATAL] AWS credentials expired mid-run.")
        print(f"  Refresh your credentials and re-run — already-deleted users will be skipped automatically.")
        print(f"  Stopped at: {resource_type} '{name}'\n")
        sys.exit(1)
    msg = f"{resource_type} '{name}': {e}"
    errors.append(msg)
    print(f"  [ERROR] {msg}")

# ─── Lambda Functions ─────────────────────────────────────────────────────────

print("── Lambda Functions ─────────────────────────────────────────────")
lam = session.client("lambda")
paginator = lam.get_paginator("list_functions")
for page in paginator.paginate():
    for fn in page["Functions"]:
        name = fn["FunctionName"]
        if is_targeted(name):
            log("Lambda", name)
            deleted.append(("Lambda", name))
            if not DRY_RUN:
                try:
                    lam.delete_function(FunctionName=name)
                except ClientError as e:
                    record_error("Lambda", name, e)

# ─── CloudWatch Log Groups ────────────────────────────────────────────────────

print("\n── CloudWatch Log Groups ────────────────────────────────────────")
logs = session.client("logs")
paginator = logs.get_paginator("describe_log_groups")
log_prefix = f"/aws/lambda/{PREFIX}"
for page in paginator.paginate(logGroupNamePrefix=log_prefix):
    for group in page["logGroups"]:
        name = group["logGroupName"]
        # Strip the /aws/lambda/ prefix before checking targeting
        fn_name = name.removeprefix("/aws/lambda/")
        if not is_targeted(fn_name):
            continue
        log("Log Group", name)
        deleted.append(("Log Group", name))
        if not DRY_RUN:
            try:
                logs.delete_log_group(logGroupName=name)
            except ClientError as e:
                record_error("Log Group", name, e)

# ─── API Gateway HTTP APIs ────────────────────────────────────────────────────

print("\n── API Gateway (HTTP APIs) ───────────────────────────────────────")
apigw = session.client("apigatewayv2")
response = apigw.get_apis()
for api in response.get("Items", []):
    name = api["Name"]
    if is_targeted(name):
        log("API Gateway", f"{name} ({api['ApiId']})")
        deleted.append(("API Gateway", name))
        if not DRY_RUN:
            try:
                apigw.delete_api(ApiId=api["ApiId"])
            except ClientError as e:
                record_error("API Gateway", name, e)

# ─── S3 Buckets ───────────────────────────────────────────────────────────────

print("\n── S3 Buckets ───────────────────────────────────────────────────")
s3 = session.client("s3")
s3_resource = session.resource("s3")
response = s3.list_buckets()
for bucket in response.get("Buckets", []):
    name = bucket["Name"]
    if is_targeted(name):
        log("S3 Bucket", name)
        deleted.append(("S3 Bucket", name))
        if not DRY_RUN:
            try:
                # Empty bucket first (required before deletion)
                b = s3_resource.Bucket(name)
                b.object_versions.delete()
                b.objects.delete()
                b.delete()
            except ClientError as e:
                record_error("S3 Bucket", name, e)

# ─── EC2 Instances ────────────────────────────────────────────────────────────

print("\n── EC2 Instances ────────────────────────────────────────────────")
ec2 = session.client("ec2")
response = ec2.describe_instances(Filters=[
    {"Name": "tag:Name", "Values": [f"{PREFIX}*"]},
    {"Name": "instance-state-name", "Values": ["pending", "running", "stopped", "stopping"]},
])
instance_ids = []
for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        iid  = instance["InstanceId"]
        name = next((t["Value"] for t in instance.get("Tags", []) if t["Key"] == "Name"), iid)
        log("EC2 Instance", f"{name} ({iid})")
        deleted.append(("EC2 Instance", name))
        instance_ids.append(iid)

if instance_ids and not DRY_RUN:
    try:
        ec2.terminate_instances(InstanceIds=instance_ids)
        print(f"  Waiting for {len(instance_ids)} instance(s) to terminate...")
        waiter = ec2.get_waiter("instance_terminated")
        waiter.wait(InstanceIds=instance_ids, WaiterConfig={"Delay": 10, "MaxAttempts": 60})
        print(f"  All instances terminated.")
    except ClientError as e:
        record_error("EC2 Instances", str(instance_ids), e)

# ─── Key Pairs ────────────────────────────────────────────────────────────────

print("\n── EC2 Key Pairs ────────────────────────────────────────────────")
response = ec2.describe_key_pairs()
for kp in response["KeyPairs"]:
    name = kp["KeyName"]
    if is_targeted(name):
        log("Key Pair", name)
        deleted.append(("Key Pair", name))
        if not DRY_RUN:
            try:
                ec2.delete_key_pair(KeyName=name)
            except ClientError as e:
                record_error("Key Pair", name, e)

# ─── Security Groups ─────────────────────────────────────────────────────────

print("\n── Security Groups ──────────────────────────────────────────────")
response = ec2.describe_security_groups(Filters=[
    {"Name": "group-name", "Values": [f"{PREFIX}*"]},
])
for sg in response["SecurityGroups"]:
    name = sg["GroupName"]
    sgid = sg["GroupId"]
    log("Security Group", f"{name} ({sgid})")
    deleted.append(("Security Group", name))
    if not DRY_RUN:
        try:
            # Step 1: detach any network interfaces still using this SG
            enis = ec2.describe_network_interfaces(Filters=[
                {"Name": "group-id", "Values": [sgid]}
            ])["NetworkInterfaces"]
            for eni in enis:
                eni_id = eni["NetworkInterfaceId"]
                attachment = eni.get("Attachment", {})
                attach_id  = attachment.get("AttachmentId")
                # Only detach non-primary attachments (index != 0)
                if attach_id and attachment.get("DeviceIndex", 0) != 0:
                    try:
                        ec2.detach_network_interface(AttachmentId=attach_id, Force=True)
                    except ClientError:
                        pass
                # Delete the ENI if it's not in-use by a running instance
                if eni.get("Status") != "in-use":
                    try:
                        ec2.delete_network_interface(NetworkInterfaceId=eni_id)
                    except ClientError:
                        pass

            # Step 2: revoke all ingress rules (some reference other SGs)
            if sg.get("IpPermissions"):
                ec2.revoke_security_group_ingress(
                    GroupId=sgid, IpPermissions=sg["IpPermissions"]
                )
            # Step 3: revoke all egress rules
            if sg.get("IpPermissionsEgress"):
                ec2.revoke_security_group_egress(
                    GroupId=sgid, IpPermissions=sg["IpPermissionsEgress"]
                )

            # Step 4: delete the security group
            ec2.delete_security_group(GroupId=sgid)

        except ClientError as e:
            record_error("Security Group", name, e)

# ─── IAM Roles (Lambda execution roles) ──────────────────────────────────────

print("\n── IAM Roles ────────────────────────────────────────────────────")
iam = session.client("iam")
paginator = iam.get_paginator("list_roles")
for page in paginator.paginate():
    for role in page["Roles"]:
        name = role["RoleName"]
        if is_targeted(name):
            log("IAM Role", name)
            deleted.append(("IAM Role", name))
            if not DRY_RUN:
                try:
                    # Detach all managed policies first
                    attached = iam.list_attached_role_policies(RoleName=name)["AttachedPolicies"]
                    for p in attached:
                        iam.detach_role_policy(RoleName=name, PolicyArn=p["PolicyArn"])
                    # Delete inline policies
                    inline = iam.list_role_policies(RoleName=name)["PolicyNames"]
                    for p in inline:
                        iam.delete_role_policy(RoleName=name, PolicyName=p)
                    iam.delete_role(RoleName=name)
                except ClientError as e:
                    record_error("IAM Role", name, e)

# ─── IAM Users ───────────────────────────────────────────────────────────────
# Deletes the IAM console user accounts for each student.
# Must run AFTER roles are cleaned up to avoid confusion with user vs role names.
# IAM users require stripping all attachments before deletion:
#   access keys → MFA devices → group memberships → policies → login profile → user

print("\n── IAM Users ────────────────────────────────────────────────────")
paginator = iam.get_paginator("list_users")
for page in paginator.paginate():
    for user in page["Users"]:
        name = user["UserName"]
        if not is_iam_user_targeted(name):
            continue
        log("IAM User", name)
        deleted.append(("IAM User", name))
        if not DRY_RUN:
            try:
                # 1. Delete access keys
                for key in iam.list_access_keys(UserName=name)["AccessKeyMetadata"]:
                    iam.delete_access_key(UserName=name, AccessKeyId=key["AccessKeyId"])

                # 2. Deactivate and delete MFA devices
                for mfa in iam.list_mfa_devices(UserName=name)["MFADevices"]:
                    iam.deactivate_mfa_device(UserName=name, SerialNumber=mfa["SerialNumber"])
                    try:
                        iam.delete_virtual_mfa_device(SerialNumber=mfa["SerialNumber"])
                    except ClientError:
                        pass  # physical MFA — skip

                # 3. Remove from all groups
                for group in iam.list_groups_for_user(UserName=name)["Groups"]:
                    iam.remove_user_from_group(GroupName=group["GroupName"], UserName=name)

                # 4. Detach managed policies
                for policy in iam.list_attached_user_policies(UserName=name)["AttachedPolicies"]:
                    iam.detach_user_policy(UserName=name, PolicyArn=policy["PolicyArn"])

                # 5. Delete inline policies
                for policy_name in iam.list_user_policies(UserName=name)["PolicyNames"]:
                    iam.delete_user_policy(UserName=name, PolicyName=policy_name)

                # 6. Delete console login profile (if exists)
                try:
                    iam.delete_login_profile(UserName=name)
                except ClientError as e:
                    if e.response["Error"]["Code"] != "NoSuchEntity":
                        raise

                # 7. Delete the user
                iam.delete_user(UserName=name)

            except ClientError as e:
                record_error("IAM User", name, e)

# ─── Summary ─────────────────────────────────────────────────────────────────

print("\n" + "─" * 60)
if DRY_RUN:
    print(f"DRY RUN complete — {len(deleted)} resource(s) would be deleted.")
    print("Run with --delete to actually remove them.\n")
else:
    print(f"Done — {len(deleted)} resource(s) deleted.")

if errors:
    print(f"\n{len(errors)} error(s):")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
