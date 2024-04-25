
import ansible_runner

# Define the S3Scanner class
class AWSRootScanner:
    def __init__(self, region, access_key, secret_key):

        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region

    def run_scan(self, private_data_dir='src/scrutinycspm/resources/playbooks/'):
        """Run the S3 bucket scan using Ansible Runner"""
        
        try:
            result = ansible_runner.run(
                playbook='aws_root_scanning.yaml',
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
            aws_account_info = result.get_fact_cache('localhost')['aws_account_info']
            
            return aws_account_info

        except Exception as e:
            # Handle the exception
            print(f"An error occurred during the AWS Root scan: {str(e)}")
            return None
        




