from azure.identity import TokenCredential
from typing import Protocol, List
from scrutinycspm.cloud.CloudResourceInventory import CloudResourceInventory
from msticpy.context.azure.azure_data import AzureData

class AzureResourceInventory(CloudResourceInventory):
    def __init__(self, tenant_id) -> None:
        self.tenant_id = tenant_id
        pass

    def authenticate(self, credential: TokenCredential) -> None:
        pass

    def get_resource_inventory(self, tenant_id: str, subscription_id: str, credential):
        
        resource_inventory is None
        try:
            # Initialize the AzureData object with the provided credential
            azure_data = AzureData()
            azure_data.credentials = credential
            # Connect to the specified Azure subscription
            azure_data.connect(tenant_id=tenant_id)

            # Get the resource inventory for the subscription
            resource_inventory = azure_data.get_resources(sub_id=subscription_id)
        except Exception as e:
            raise Exception(f"An error occurred while getting the resource inventory: {str(e)}") from e
        
        return resource_inventory
           