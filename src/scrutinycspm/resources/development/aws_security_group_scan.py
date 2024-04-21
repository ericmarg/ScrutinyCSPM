import json
import ansible_runner

class AWSSecurityGroupScanner:
    def __init__(self, region, access_key, secret_key):

        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region

    def run_scan(self, private_data_dir='src/scrutinycspm/resources/playbooks/'):
        """Run the security group scan using Ansible Runner"""
        
        try:
            result = ansible_runner.run(
                playbook='aws_security_group_scanning.yaml',
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
            security_groups_json = result.get_fact_cache('localhost')['security_groups_json']
            
            return security_groups_json

        except Exception as e:
            # Handle the exception
            print(f"An error occurred during the Security Group scan: {str(e)}")
            return None
        