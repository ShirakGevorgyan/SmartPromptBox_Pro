variable "aws_region" {
    description = "AWS region or LocalStack's region"
    type        = string
    default     = "us-east-1"
}

variable "aws_endpoint_url" {
    description = "LocalStack endpoint like http://localhost:4566 (empty for real AWS)"
    type        = string
    default     = ""
}

variable "artifact_bucket_name" {
    description = "S3 bucket name for CI artifacts demo"
    type        = string
    default     = "spb-ci-artifacts-demo"
}
