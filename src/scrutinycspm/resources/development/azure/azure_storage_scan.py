
import ansible_runner
from azure.storage.blob import BlobServiceClient

from src.scrutinycspm.utils.logging_util import add_logging

class AzureStorageScanner:
    def __init__(self, subscription_id, tenant_id, client_id, client_secret):
        self.subscription_id = subscription_id
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret

    @add_logging
    def run_scan(self, private_data_dir='src/scrutinycspm/resources/playbooks/azure/'):
        """Run the RDS bucket scan using Ansible Runner"""
        try:
            result = ansible_runner.run(
                playbook='az_storage_scanning.yaml',
                inventory=None,
                private_data_dir=private_data_dir,
                quiet=True,
                extravars={
                    'subscription_id': self.subscription_id,
                    'tenant_id': self.tenant_id,
                    'client_id': self.client_id,
                    'client_secret': self.client_secret
                }
            )

            test = result.get_fact_cache('localhost')

            # Retrieve the JSON data from the fact cache
            azure_storage_accounts = result.get_fact_cache('localhost')['azure_storage_accounts']
            
            return azure_storage_accounts

        except Exception as e:
            # Handle the exception
            print(f"An error occurred during the Azure Storage scan: {str(e)}")
            return None
