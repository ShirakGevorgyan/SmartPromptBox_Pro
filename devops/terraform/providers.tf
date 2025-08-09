terraform {
    required_version = ">= 1.6.0"
    required_providers {
    aws = {
        source  = "hashicorp/aws"
        version = "~> 5.0"
    }
    }
}

# By default works against real AWS creds (not used in CI).
# For LocalStack locally:
# export AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1
# export AWS_ENDPOINT_URL=http://localhost:4566
provider "aws" {
    region = var.aws_region

# If AWS_ENDPOINT_URL is set (LocalStack), use it.
    endpoints {
    s3 = try(regex("^http", var.aws_endpoint_url) != null ? var.aws_endpoint_url : null, null)
    }

    s3_use_path_style = true
}
