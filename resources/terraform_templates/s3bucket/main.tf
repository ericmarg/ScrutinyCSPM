provider "aws" {
  region = "us-east-2"  # Replace with your desired AWS region
}

# Create a bucket with private access
resource "aws_s3_bucket" "private-bucket-02" {
  bucket = "my-private-bucket-02" # Replace with your desired bucket name
}

resource "aws_s3_bucket_ownership_controls" "private_bucket_ownership" {
  bucket = aws_s3_bucket.private-bucket-02.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

# Create a bucket with public read access
resource "aws_s3_bucket" "public_read_bucket-02" {
  bucket = "my-public-read-bucket-02" # Replace with your desired bucket name
}

resource "aws_s3_bucket_public_access_block" "public_read_bucket_access" {
  bucket = aws_s3_bucket.public_read_bucket-02.id

  block_public_acls       = false
  block_public_policy     = true
  ignore_public_acls      = false
  restrict_public_buckets = true
}

resource "aws_s3_bucket_ownership_controls" "public_read_bucket_ownership" {
  bucket = aws_s3_bucket.public_read_bucket-02.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

# Create a bucket with public read and write access
resource "aws_s3_bucket" "public_read_write_bucket-02" {
  bucket = "my-public-read-write-bucket-02" # Replace with your desired bucket name
}

resource "aws_s3_bucket_public_access_block" "public_read_write_bucket_access" {
  bucket = aws_s3_bucket.public_read_write_bucket-02.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}