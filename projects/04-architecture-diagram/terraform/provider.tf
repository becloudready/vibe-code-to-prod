terraform {
  required_version = ">= 1.3"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project   = "arcflow"
      Student   = var.student_name
      ManagedBy = "terraform"
    }
  }
}

data "aws_caller_identity" "current" {}
