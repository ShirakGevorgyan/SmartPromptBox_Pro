output "artifact_bucket" {
    value       = aws_s3_bucket.artifacts.bucket
    description = "Name of the S3 bucket for artifacts"
}
