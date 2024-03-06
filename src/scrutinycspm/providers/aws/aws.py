import boto3
import botocore.exceptions

s3 = boto3.client('s3')

buckets_list = s3.list_buckets() # gathers all S3 buckets in target account
public_access_block_dict = {}

# loops through all buckets, obtaining the PublicAccessBlock Configuration
for bucket in buckets_list['Buckets']:
    bucket_name = bucket['Name']

    try:
        response = s3.get_public_access_block(
            Bucket=bucket_name
        )
        public_access_block_dict[bucket_name] = response['PublicAccessBlockConfiguration']
    except botocore.exceptions.ClientError: # handles case where 'Block All Public Access' is OFF
        public_access_block_dict[bucket_name] = '{}'

print('Public Access Block Configuration dictionary (S3 bucket names are the key:)')
print(public_access_block_dict)
print('End of S3 Report\n')
