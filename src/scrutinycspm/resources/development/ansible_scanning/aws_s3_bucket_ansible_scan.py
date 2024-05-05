import ansible_runner
import json
import configparser
import os

# Define the S3Scanner class
class AWSS3Scanner:
    def __init__(self, region, access_key, secret_key):

        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region

    def run_scan(self, private_data_dir='src/scrutinycspm/resources/playbooks/'):
        """Run the RDS bucket scan using Ansible Runner"""

        try:
            result = ansible_runner.run(
                playbook='aws_s3_scanning_opa.yaml',
                suppress_ansible_output=True,
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
            rego_policy_content = result.get_fact_cache('localhost')['rego_policy_content']

            raw_s3_results = result.get_fact_cache('localhost')['raw_s3_results']

            return  raw_s3_results, rego_policy_content

        except Exception as e:
            # Handle the exception
            print(f"An error occurred during the S3 Bucket scan: {str(e)}")
            return None

