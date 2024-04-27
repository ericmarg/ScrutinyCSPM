import boto3
import json

class S3BucketRetriever:
    def __init__(self, access_key, secret_key, region):
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.s3_client = None

    def setup_s3_client(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region
        )

    def get_s3_bucket_details(self, bucket_name):
        if self.s3_client is None:
            self.setup_s3_client()

        bucket_details = {}

        try:
            # Retrieve bucket policy
            try:
                policy = self.s3_client.get_bucket_policy(Bucket=bucket_name)
                bucket_details['Policy'] = json.loads(policy['Policy'])
            except self.s3_client.exceptions.NoSuchBucketPolicy:
                bucket_details['Policy'] = None

            # Retrieve bucket ACL
            acl = self.s3_client.get_bucket_acl(Bucket=bucket_name)
            bucket_details['ACL'] = acl['Grants']

            # Retrieve bucket encryption settings
            try:
                encryption = self.s3_client.get_bucket_encryption(Bucket=bucket_name)
                bucket_details['Encryption'] = encryption['ServerSideEncryptionConfiguration']['Rules']
            except self.s3_client.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                    bucket_details['Encryption'] = None
                else:
                    raise

            # Retrieve bucket versioning status
            versioning = self.s3_client.get_bucket_versioning(Bucket=bucket_name)
            bucket_details['Versioning'] = versioning.get('Status')

        except self.s3_client.exceptions.NoSuchBucket:
            print(f"Bucket '{bucket_name}' does not exist.")
        except Exception as e:
            print(f"Error retrieving details for bucket '{bucket_name}': {str(e)}")

        return bucket_details

    def get_s3_buckets(self):
        if self.s3_client is None:
            self.setup_s3_client()

        try:
            response = self.s3_client.list_buckets()
            buckets = []
            for bucket in response['Buckets']:
                bucket_name = bucket['Name']
                bucket_details = self.get_s3_bucket_details(bucket_name)
                buckets.append({
                    'Name': bucket_name,
                    'Details': bucket_details
                })
            return buckets
        except Exception as e:
            print(f"Error retrieving S3 buckets: {str(e)}")
            return []

    def run_scan(self):
        buckets = self.get_s3_buckets()
        scan_results = {
            'S3Buckets': buckets
        }
        return json.dumps(scan_results, default=str)

