import json
import os
from typing import Dict, Type
from cli.commands.command_manager import CommandPlugin, SubCommandPlugin
from src.scrutinycspm.resources.development.azure.azure_nsg_scan import AzureNetworkSecurityGroup
from src.scrutinycspm.resources.development.azure.azure_storage_scan import AzureStorageAccount
from src.scrutinycspm.resources.development.azure.azure_vnet_scan import AzureVirtualNetwork
from src.scrutinycspm.resources.development.azure.azure_virtual_machine_scan import AzureVirtualMachine
from src.scrutinycspm.utils.logging_util import add_logging
from src.scrutinycspm.providers.azure.policy_check import vulernabilities


class Nsg(SubCommandPlugin):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def execute(self, *args, **kwargs):
        
        subscription_id = os.environ.get('AZURE_SUBSCRIPTION_ID')
        tenant_id = os.environ.get('AZURE_TENANT')
        client_id = os.environ.get('AZURE_CLIENT_ID')
        client_secret = os.environ.get('AZURE_SECRET')
        client_certificate = None

        if not subscription_id or not tenant_id or not client_id or not client_secret:
            raise ValueError("Missing required environment variables: AZURE_SUBSCRIPTION_ID, AZURE_TENANT, AZURE_CLIENT_ID, AZURE_SECRET")

        nsg_scanner = AzureNetworkSecurityGroup(subscription_id, tenant_id, client_id, client_secret, client_certificate)
        json_data = nsg_scanner.fetch_data()
        data = json.loads(json_data)
        json_data = json.dumps(data, indent=4)  

        if len(args) > 0 and args[0] == 'scan':
            vulernabilities_json_data = vulernabilities(json_data, "azure.nsg", "policies/azure/nsg.rego")

            return json_data, vulernabilities_json_data
        return json_data, None

class VirtualMachine(SubCommandPlugin):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def execute(self, *args, **kwargs):
        subscription_id = os.environ.get('AZURE_SUBSCRIPTION_ID')
        tenant_id = os.environ.get('AZURE_TENANT')
        client_id = os.environ.get('AZURE_CLIENT_ID')
        client_secret = os.environ.get('AZURE_SECRET')
        client_certificate = None

        if not subscription_id or not tenant_id or not client_id or not client_secret:
            raise ValueError("Missing required environment variables: AZURE_SUBSCRIPTION_ID, AZURE_TENANT, AZURE_CLIENT_ID, AZURE_SECRET")

        vm_scanner = AzureVirtualMachine(subscription_id, tenant_id, client_id, client_secret, client_certificate)
        json_data = vm_scanner.fetch_data()
        data = json.loads(json_data)
        json_data = json.dumps(data, indent=4)  

        if len(args) > 0 and args[0] == 'scan':
            vulernabilities_json_data = vulernabilities(json_data, "azure.nsg", "policies/azure/nsg.rego")

            return json_data, vulernabilities_json_data
        return json_data, None
    
class StorageAccount(SubCommandPlugin):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def execute(self, *args, **kwargs):
        subscription_id = os.environ.get('AZURE_SUBSCRIPTION_ID')
        tenant_id = os.environ.get('AZURE_TENANT')
        client_id = os.environ.get('AZURE_CLIENT_ID')
        client_secret = os.environ.get('AZURE_SECRET')
        client_certificate = None

        if not subscription_id or not tenant_id or not client_id or not client_secret:
            raise ValueError("Missing required environment variables: AZURE_SUBSCRIPTION_ID, AZURE_TENANT, AZURE_CLIENT_ID, AZURE_SECRET")

        storage_scanner = AzureStorageAccount(subscription_id, tenant_id, client_id, client_secret, client_certificate)
        json_data = storage_scanner.fetch_data()
        data = json.loads(json_data)
        json_data = json.dumps(data, indent=4)  

        if len(args) > 0 and args[0] == 'scan':
            vulernabilities_json_data = vulernabilities(json_data, "azure.nsg", "policies/azure/nsg.rego")

            return json_data, vulernabilities_json_data
        return json_data, None
        
class Vnet(SubCommandPlugin):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def execute(self, *args, **kwargs):
        subscription_id = os.environ.get('AZURE_SUBSCRIPTION_ID')
        tenant_id = os.environ.get('AZURE_TENANT')
        client_id = os.environ.get('AZURE_CLIENT_ID')
        client_secret = os.environ.get('AZURE_SECRET')
        client_certificate = None

        if not subscription_id or not tenant_id or not client_id or not client_secret:
            raise ValueError("Missing required environment variables: AZURE_SUBSCRIPTION_ID, AZURE_TENANT, AZURE_CLIENT_ID, AZURE_SECRET")

        vnet_scanner = AzureVirtualNetwork(subscription_id, tenant_id, client_id, client_secret, client_certificate)
        json_data = vnet_scanner.fetch_data()
        data = json.loads(json_data)
        json_data = json.dumps(data, indent=4)  

        if len(args) > 0 and args[0] == 'scan':
            vulernabilities_json_data = vulernabilities(json_data, "azure.nsg", "policies/azure/nsg.rego")

            return json_data, vulernabilities_json_data
        return json_data, None
    
        
@add_logging
class AzureRootCommand(CommandPlugin):
    
    def __init__(self, *args, **kwargs):
        self.subcommands: Dict[str, Type[CommandPlugin]] = {
        "nsg": Nsg,
        "vm": VirtualMachine,
        "vnet": Vnet,
        "storage" : StorageAccount
    }

    def execute(self, args, *kwargs) -> any:
        subscription_id = os.environ.get('AZURE_SUBSCRIPTION_ID')
        tenant_id = os.environ.get('AZURE_TENANT')
        client_id = os.environ.get('AZURE_CLIENT_ID')
        client_secret = os.environ.get('AZURE_SECRET')
        client_certificate = None

        if not subscription_id or not tenant_id or not client_id or not client_secret:
            raise ValueError("Missing required environment variables: AZURE_SUBSCRIPTION_ID, AZURE_TENANT, AZURE_CLIENT_ID, AZURE_SECRET")

        nsg_scanner = AzureNetworkSecurityGroup(subscription_id, tenant_id, client_id, client_secret, client_certificate)
        json_data = nsg_scanner.fetch_data()
        return json_data

    def help(self) -> str:
        return "Scans Azure Network Security Groups and retrieves their security details."