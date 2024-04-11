import boto3
from abc import ABC, abstractmethod
from src.scrutinycspm.resources.resource import Resource
from src.scrutinycspm.utils.development.resource_generator import generate_resource_classes

s3_client = boto3.client('s3')

# List all S3 buckets
response = s3_client.list_buckets()


buckets = response['Buckets']
for bucket in buckets:
    print(f"Bucket Name: {bucket['Name']}")

