import json
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient

from src.scrutinycspm.resources.azure_resource import AzureResource

class AzureVirtualMachine(AzureResource):
    """
    Represents an Azure Virtual Machine resource.

    Attributes:
        subscription_id (str): The subscription ID for the Azure resource.
        tenant_id (str): The tenant ID for the Azure resource.
        client_id (str): The client ID for accessing the Azure resource.
        client_secret (str): The client secret for accessing the Azure resource.
        client_certificate (str): The client certificate for accessing the Azure resource.
    """

    def __init__(self, subscription_id, tenant_id, client_id, client_secret, client_certificate):
        self.subscription_id = subscription_id
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.client_certificate = client_certificate

    def fetch_data(self):
        """
        Fetch Azure Virtual Machine data from the Azure Management API.

        Returns:
            str: JSON string representing the list of Azure Virtual Machines and their details.
        """
        virtual_machines = self.get_all_virtual_machines(
            tenant_id=self.tenant_id,
            subscription_id=self.subscription_id,
            client_id=self.client_id,
            client_secret=self.client_secret
        )

        virtual_machine_details = []
        for vm in virtual_machines:
            credential = ClientSecretCredential(
                tenant_id=self.tenant_id,
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            compute_client = ComputeManagementClient(credential, self.subscription_id)

            vm_details = compute_client.virtual_machines.get(
                resource_group_name=vm.id.split('/')[4],
                vm_name=vm.name
            )

            virtual_machine_details.append({
                'id': vm.id,
                'name': vm.name,
                'resource_group': vm.id.split('/')[4],
                'location': vm.location,
                'vm_size': vm_details.hardware_profile.vm_size,
                'os_type': vm_details.storage_profile.os_disk.os_type,
                'os_disk_name': vm_details.storage_profile.os_disk.name,
                'os_disk_caching': vm_details.storage_profile.os_disk.caching,
                'provisioning_state': vm_details.provisioning_state,
                'data_disks': [{
                    'name': disk.name,
                    'size_gb': disk.disk_size_gb,
                    'caching': disk.caching.value
                } for disk in vm_details.storage_profile.data_disks]
            })

        return json.dumps(virtual_machine_details, indent=4)

    @staticmethod
    def get_all_virtual_machines(tenant_id, subscription_id, client_id, client_secret):
        """
        Retrieve all Azure Virtual Machines for the given Azure Tenant, Subscription, Client ID, and Secret.

        Returns:
            list: A list of Azure Virtual Machine objects.
        """
        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )
        compute_client = ComputeManagementClient(credential, subscription_id)

        return list(compute_client.virtual_machines.list_all())