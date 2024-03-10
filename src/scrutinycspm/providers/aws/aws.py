"""AWS Provider: Gets Public Access Block Configuration for S3 buckets"""

import json
import boto3
import botocore.exceptions

s3 = boto3.client('s3')

buckets_list = s3.list_buckets() # gathers all S3 buckets in target account
public_access_block_dict = {}
encryption_dict = {}
bucket_versioning_dict = {}

# loops through all buckets, obtaining the PublicAccessBlock Configuration
for bucket in buckets_list['Buckets']:
    bucket_name = bucket['Name']

    try:
        response = s3.get_public_access_block(Bucket=bucket_name)
        public_access_block_dict[bucket_name] = response['PublicAccessBlockConfiguration']
    except botocore.exceptions.ClientError: # handles case where 'Block All Public Access' is OFF
        public_access_block_dict[bucket_name] = '{}'

    try:
        bucket_versioning_status = s3.get_bucket_versioning(Bucket=bucket_name)['Status']
        bucket_versioning_dict[bucket_name] = bucket_versioning_status
    except KeyError: # handles case where 'Bucket versioning' has never been turned on
        bucket_versioning_dict[bucket_name] = '{}'

print('Public Access Block report')
print(json.dumps(public_access_block_dict))
print()
print('Bucket Versioning report')
print(json.dumps(bucket_versioning_dict))
print()
print('End of S3 Report\n')
