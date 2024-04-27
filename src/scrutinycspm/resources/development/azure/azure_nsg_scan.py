import json
from azure.identity import ClientSecretCredential
from azure.mgmt.network import NetworkManagementClient
import logging
from src.scrutinycspm.resources.azure_resource import AzureResource

# Configure the logging level to suppress INFO messages
logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.WARNING)
logging.getLogger("azure.identity._internal.get_token_mixin").setLevel(logging.WARNING)

class AzureNetworkSecurityGroup(AzureResource):
    """
    Represents an Azure Network Security Group resource.

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
        Fetch Azure Network Security Group data from the Azure Management API.

        Returns:
            str: JSON string representing the list of Azure Network Security Groups and their details.
        """
        network_security_groups = self.get_all_network_security_groups(
            tenant_id=self.tenant_id,
            subscription_id=self.subscription_id,
            client_id=self.client_id,
            client_secret=self.client_secret
        )

        network_security_group_details = []
        for nsg in network_security_groups:
            credential = ClientSecretCredential(
                tenant_id=self.tenant_id,
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            network_client = NetworkManagementClient(credential, self.subscription_id)

            nsg_details = network_client.network_security_groups.get(
                resource_group_name=nsg.id.split('/')[4],
                network_security_group_name=nsg.name
            )

            network_security_group_details.append({
                'id': nsg.id,
                'name': nsg.name,
                'resource_group': nsg.id.split('/')[4],
                'location': nsg.location,
                'security_rules': [{
                    'name': rule.name,
                    'description': rule.description,
                    'protocol': rule.protocol,
                    'source_port_range': rule.source_port_range,
                    'destination_port_range': rule.destination_port_range,
                    'source_address_prefix': rule.source_address_prefix,
                    'destination_address_prefix': rule.destination_address_prefix,
                    'access': rule.access,
                    'priority': rule.priority,
                    'direction': rule.direction
                } for rule in nsg_details.security_rules],
                'default_security_rules': [{
                    'name': rule.name,
                    'description': rule.description,
                    'protocol': rule.protocol,
                    'source_port_range': rule.source_port_range,
                    'destination_port_range': rule.destination_port_range,
                    'source_address_prefix': rule.source_address_prefix,
                    'destination_address_prefix': rule.destination_address_prefix,
                    'access': rule.access,
                    'priority': rule.priority,
                    'direction': rule.direction
                } for rule in nsg_details.default_security_rules]
            })

        return json.dumps(network_security_group_details, indent=4)

    @staticmethod
    def get_all_network_security_groups(tenant_id, subscription_id, client_id, client_secret):
        """
        Retrieve all Azure Network Security Groups for the given Azure Tenant, Subscription, Client ID, and Secret.

        Returns:
            list: A list of Azure Network Security Group objects.
        """
        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )
        network_client = NetworkManagementClient(credential, subscription_id)

        return list(network_client.network_security_groups.list_all())