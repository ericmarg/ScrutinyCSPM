
import boto3
from botocore.exceptions import ClientError

# Define the S3Scanner class
class AWSRootScanner:
    def __init__(self, region, access_key, secret_key):

        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region

    def run_scan(self):      
        try:
            account_info = self.get_aws_account_info(self.access_key, self.secret_key, self.region)
            return account_info

        except Exception as e:
            # Handle the exception
            return f"An error occurred during the AWS Root scan: {str(e)}"
        


    def get_aws_account_info(self, aws_access_key, aws_secret_key, aws_region):
        try:
            # Create boto3 clients
            sts_client = boto3.client('sts', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)
            ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)
            s3_client = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

            # Get AWS Account ID
            aws_account_info = sts_client.get_caller_identity()
            account_id = aws_account_info['Account']

            # Get AWS EC2 Instance Count
            ec2_instances = ec2_client.describe_instances()
            ec2_instance_count = sum(len(reservation['Instances']) for reservation in ec2_instances['Reservations'])

            # Get AWS S3 Bucket Count
            s3_buckets = s3_client.list_buckets()
            s3_bucket_count = len(s3_buckets['Buckets'])

            # Get AWS VPC Count
            vpcs = ec2_client.describe_vpcs()
            vpc_count = len(vpcs['Vpcs'])

            # Get AWS Security Group Count
            security_groups = ec2_client.describe_security_groups()
            security_group_count = len(security_groups['SecurityGroups'])

            # Store AWS Account Information in a dictionary
            aws_account_info = {
                'account_id': account_id,
                'ec2_instance_count': ec2_instance_count,
                's3_bucket_count': s3_bucket_count,
                'vpc_count': vpc_count,
                'security_group_count': security_group_count
            }

            return aws_account_info

        except ClientError as e:
            print("An error occurred:", e)
            return None



