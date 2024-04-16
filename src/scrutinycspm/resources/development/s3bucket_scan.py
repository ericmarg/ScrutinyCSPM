
import ansible_runner
import json
import configparser
import os

# Define the S3Scanner class
class S3Scanner:
    def __init__(self, region, access_key, secret_key):

        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region

    def run_scan(self, private_data_dir='src/scrutinycspm/resources/development/playbooks/'):
        """Run the S3 bucket scan using Ansible Runner"""
        
        try:
            result = ansible_runner.run(
                playbook='s3_scanning.yaml',
                inventory=None,
                private_data_dir= private_data_dir,
                quiet=True,
                extravars={
                    'aws_access_key': self.access_key,
                    'aws_secret_key': self.secret_key,
                    'aws_region': self.region
                }
            )

            # Retrieve the JSON data from the fact cache
            ec2_security_json = result.get_fact_cache('localhost')['s3_buckets_info']
            
            return ec2_security_json

        except Exception as e:
            # Handle the exception
            print(f"An error occurred during the EC2 scan: {str(e)}")
            return None
        



