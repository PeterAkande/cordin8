terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.34.0"
    }

    random = {
      source  = "hashicorp/random"
      version = "3.6.0"
    }

    archive = {
      source  = "hashicorp/archive"
      version = "2.4.2"
    }
  }
}


provider "aws" {
  shared_credentials_files = ["~/.aws/credentials"]
  profile                  = "authivate"
  region                   = "us-west-2"
}
