provider "aws" {
  region = "us-west-2"  # Replace with your desired AWS region
}

# Create a bucket with private access
resource "aws_s3_bucket" "private-bucket-01" {
  bucket = "my-private-bucket-01" # Replace with your desired bucket name
}

resource "aws_s3_bucket_ownership_controls" "private_bucket_ownership" {
  bucket = aws_s3_bucket.private-bucket-01.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}