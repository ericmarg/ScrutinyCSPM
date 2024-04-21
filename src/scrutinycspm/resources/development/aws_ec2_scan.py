from src.scrutinycspm.utils.development.resource_generator import generate_resource_classes
import ansible_runner
import json
import configparser
import os
from src.scrutinycspm.utils.development.resource_generator import generate_resource_classes

# Define the EC2Scanner class
class AWSEC2Scanner:
    def __init__(self, region, access_key, secret_key):

        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region

    def run_scan(self, private_data_dir='src/scrutinycspm/resources/playbooks/'):

        test = os.getcwd()
        try:
            result = ansible_runner.run(
                playbook='aws_ec2_scanning.yaml',
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
            ec2_security_json = result.get_fact_cache('localhost')['ec2_config_cache']
            return ec2_security_json

        except Exception as e:
            # Handle the exception
            print(f"An error occurred during the EC2 scan: {str(e)}")
            return None
        

