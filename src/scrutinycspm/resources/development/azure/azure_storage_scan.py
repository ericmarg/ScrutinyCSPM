import json
from azure.identity import ClientSecretCredential
from azure.mgmt.storage import StorageManagementClient
from src.scrutinycspm.resources.azure_resource import AzureResource

class AzureStorageAccount(AzureResource):
    """
    Represents an Azure Storage Account resource.

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
        Fetch Azure Storage Account data from the Azure Management API.

        Returns:
            str: JSON string representing the list of Azure Storage Accounts and their details.
        """
        storage_accounts = self.get_all_storage_accounts(
            tenant_id=self.tenant_id,
            subscription_id=self.subscription_id,
            client_id=self.client_id,
            client_secret=self.client_secret
        )

        storage_account_details = []
        for storage_account in storage_accounts:
            credential = ClientSecretCredential(
                tenant_id=self.tenant_id,
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            storage_client = StorageManagementClient(credential, self.subscription_id)
            account_details = storage_client.storage_accounts.get_properties(
                resource_group_name=storage_account.id.split('/')[4],
                account_name=storage_account.name
            )

            # Get versioning information
            blob_service_properties = storage_client.blob_services.get_service_properties(
                resource_group_name=storage_account.id.split('/')[4],
                account_name=storage_account.name
            )
            versioning_enabled = blob_service_properties.is_versioning_enabled

            storage_account_details.append({
                'id': storage_account.id,
                'name': storage_account.name,
                'resource_group': storage_account.id.split('/')[4],
                'location': storage_account.location,
                'sku': account_details.sku.name,
                'kind': account_details.kind,
                'encryption_enabled': account_details.encryption.services.blob.enabled,
                'https_only': account_details.enable_https_traffic_only,
                'allow_blob_public_access': account_details.allow_blob_public_access,
                'network_rule_set': {
                    'default_action': account_details.network_rule_set.default_action,
                    'ip_rules': [rule.ip_address_or_range for rule in account_details.network_rule_set.ip_rules],
                    'virtual_network_rules': [rule.virtual_network_resource_id for rule in account_details.network_rule_set.virtual_network_rules]
                },
                'versioning_enabled': versioning_enabled,
                'public_network_access': account_details.public_network_access,
                'minimum_tls_version': account_details.minimum_tls_version,
                'allow_shared_key_access': account_details.allow_shared_key_access
            })

        return json.dumps(storage_account_details, indent=4)

    @staticmethod
    def get_all_storage_accounts(tenant_id, subscription_id, client_id, client_secret):
        """
        Retrieve all Azure Storage Accounts for the given Azure Tenant, Subscription, Client ID, and Secret.

        Returns:
            list: A list of Azure Storage Account objects.
        """
        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )
        storage_client = StorageManagementClient(credential, subscription_id)
        return list(storage_client.storage_accounts.list())