import ansible_runner
import json

from src.scrutinycspm.utils.development.resource_generator import generate_resource_classes

# Run playbook1.yml
result = ansible_runner.run(
    playbook='/home/robert/Documents/python_projects/scrutinycspm/ScrutinyCSPM/src/scrutinycspm/utils/development/playbook3.yaml',
    inventory=None,
    quiet=True
)

# Access the s3_buckets_info variable from the fact cache
s3_buckets_info = result.get_fact_cache('localhost')['s3_buckets_info']

# Generate resource classes for S3 buckets
s3_resource_classes = generate_resource_classes(s3_buckets_info, 'S3Bucket')

# Process the S3 bucket information
for bucket in s3_buckets_info:
    print(f"Bucket Name: {bucket['name']}")
    print(f"Creation Date: {bucket['creation_date']}")
    print(f"Encryption: {bucket.get('encryption', {}).get('rules', 'None')}")
    print(f"Public Access Block: {bucket.get('public_access_block', 'None')}")
    print(f"Versioning: {bucket.get('versioning', {}).get('status', 'Disabled')}")
    print('---')