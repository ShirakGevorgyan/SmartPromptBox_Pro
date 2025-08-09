resource "aws_s3_bucket" "artifacts" {
    bucket = var.artifact_bucket_name
    tags = {
    project = "SmartPromptBox_Pro"
    managed = "terraform"
    }
}