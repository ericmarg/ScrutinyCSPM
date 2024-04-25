
import ansible_runner

# Define the S3Scanner class
class AWSRDSScanner:
    def __init__(self, region, access_key, secret_key):

        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region

    def run_scan(self, private_data_dir='src/scrutinycspm/resources/playbooks/'):
        
        """Run the RDS bucket scan using Ansible Runner"""
        
        try:
            result = ansible_runner.run(
                playbook='aws_rds_mysql_scanning.yaml',
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
            rds_databases_json = result.get_fact_cache('localhost')['rds_databases_json']
            
            return rds_databases_json

        except Exception as e:
            # Handle the exception
            print(f"An error occurred during the S3 Bucket scan: {str(e)}")
            return None
        




