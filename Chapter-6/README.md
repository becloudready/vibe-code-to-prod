# Chapter 6 — Cloud, Infrastructure & CI/CD

## Overview

This chapter covers the concepts and hands-on skills needed to provision cloud infrastructure, automate deployments, and build serverless APIs. Students will launch a real EC2 instance, deploy a web server with GitHub Actions, trigger Lambda functions from S3 events, and expose a Lambda function as a REST API using API Gateway.

---

## Lab

| File | Description |
|------|-------------|
| [Lab — Deploy to EC2 with CI/CD](./Lab-Deploy-EC2-CICD.md) | End-to-end lab: launch EC2 with Terraform, deploy nginx with a shell script, then automate with GitHub Actions |
| [Lab — Lambda S3 Trigger](./Lab-Lambda-S3-Trigger.md) | Serverless lab: create an S3 bucket, trigger a Lambda function on file upload, view logs in CloudWatch |
| [Lab — Lambda REST API](./Lab-Lambda-REST-API.md) | Serverless API lab: expose a Lambda function as a REST API using API Gateway with GET and POST endpoints |


---

## Prerequisites

- [ ] AWS CLI installed and configured (`aws configure`)
- [ ] Terraform installed (`terraform -version`)
- [ ] Git installed and GitHub account ready
- [ ] AWS IAM user with student policies attached (see [IAM-Student-Policies.md](./IAM-Student-Policies.md))
