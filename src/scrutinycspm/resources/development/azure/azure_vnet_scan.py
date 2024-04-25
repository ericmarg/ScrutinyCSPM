import json
from azure.identity import ClientSecretCredential
from azure.mgmt.network import NetworkManagementClient

from src.scrutinycspm.resources.azure_resource import AzureResource

class AzureVirtualNetwork(AzureResource):
    """
    Represents an Azure Virtual Network resource.

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
        Fetch Azure Virtual Network data from the Azure Management API.

        Returns:
            str: JSON string representing the list of Azure Virtual Networks and their details.
        """
        virtual_networks = self.get_all_virtual_networks(
            tenant_id=self.tenant_id,
            subscription_id=self.subscription_id,
            client_id=self.client_id,
            client_secret=self.client_secret
        )

        virtual_network_details = []
        for vnet in virtual_networks:
            credential = ClientSecretCredential(
                tenant_id=self.tenant_id,
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            network_client = NetworkManagementClient(credential, self.subscription_id)

            vnet_details = network_client.virtual_networks.get(
                resource_group_name=vnet.id.split('/')[4],
                virtual_network_name=vnet.name
            )

            virtual_network_details.append({
                'id': vnet.id,
                'name': vnet.name,
                'resource_group': vnet.id.split('/')[4],
                'location': vnet.location,
                'address_space': vnet_details.address_space.address_prefixes,
                'subnets': [{
                    'name': subnet.name,
                    'address_prefix': subnet.address_prefix,
                    'network_security_group': subnet.network_security_group.id if subnet.network_security_group else None,
                    'route_table': subnet.route_table.id if subnet.route_table else None,
                    'service_endpoints': [endpoint.service for endpoint in subnet.service_endpoints] if subnet.service_endpoints else [],
                    'private_endpoint_network_policies': subnet.private_endpoint_network_policies,
                    'private_link_service_network_policies': subnet.private_link_service_network_policies
                } for subnet in vnet_details.subnets],
                'enable_ddos_protection': vnet_details.enable_ddos_protection,
                'enable_vm_protection': vnet_details.enable_vm_protection,
                'dns_servers': vnet_details.dhcp_options.dns_servers if vnet_details.dhcp_options else [],
                'flow_timeout_in_minutes': vnet_details.flow_timeout_in_minutes
            })

        return json.dumps(virtual_network_details, indent=4)

    @staticmethod
    def get_all_virtual_networks(tenant_id, subscription_id, client_id, client_secret):
        """
        Retrieve all Azure Virtual Networks for the given Azure Tenant, Subscription, Client ID, and Secret.

        Returns:
            list: A list of Azure Virtual Network objects.
        """
        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )
        network_client = NetworkManagementClient(credential, subscription_id)

        return list(network_client.virtual_networks.list_all())