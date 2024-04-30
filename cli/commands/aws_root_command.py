import logging
import os
from typing import Dict, Type

from cli.commands.command_manager import CommandPlugin, SubCommandPlugin
from hydra import compose, initialize
from src.scrutinycspm.access.repository.github_provider import GitHubRepository
from hydra.core.global_hydra import GlobalHydra
from src.scrutinycspm.providers.azure.azure_policy_check import vulernabilities
from src.scrutinycspm.resources.development.aws_ec2_scan import EC2InstanceRetriever
from src.scrutinycspm.resources.development.aws_rds_scan import RDSMySQLDatabaseRetriever
from src.scrutinycspm.resources.development.aws_s3bucket_scan import S3BucketRetriever
from src.scrutinycspm.resources.development.aws_security_group_scan import AWSSecurityGroupScanner
from src.scrutinycspm.utils.logging_util import add_logging
from src.scrutinycspm.resources.development.aws_root_scan import AWSRootScanner
from src.scrutinycspm.utils.aws_credential_file import get_aws_credentials
from opa_client.opa import OpaClient
from opa_client.errors import ConnectionsError

class Root(SubCommandPlugin):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def execute(self, *args, **kwargs):
        access_key, secret_key, profile = get_aws_credentials()
        region = args[0]
        json_data = AWSRootScanner(region=region, access_key=access_key, secret_key=secret_key).run_scan()

        if len(args) > 0 and args[0] == 'scan':
            vulernabilities_json_data = vulernabilities(json_data, "azure.nsg", "policies/azure/nsg.rego")

            return json_data, vulernabilities_json_data
        return json_data, None


    def rego_policy_check(self, verify_objects, region, policy_path, *args, **kwargs):
        opa = OpaClient()

        for container in verify_objects:
            
            container_dict = container.to_dict() # formats the object model to a dict to be sent to OPA
            decisions = []

            access_key, secret_key, profile = get_aws_credentials()

            opa.update_opa_policy_fromfile(filepath="../../policies/object_storage.rego", endpoint="obj_storage")
            versioning_decision = opa.check_policy_rule(input_data=container_dict, package_path='obj_storage', rule_name='enforce_versioning_enabled')
            decisions.append(versioning_decision)
            public_access_block_decision = opa.check_policy_rule(input_data=container_dict, package_path='obj_storage', rule_name='enforce_public_access_block')
            decisions.append(public_access_block_decision)
            mfa_delete_decision = opa.check_policy_rule(input_data=container_dict, package_path='obj_storage', rule_name='enforce_aws_s3_mfa_enabled')
            decisions.append(mfa_delete_decision)
            print(f'Object Storage Container: {container.name}, Versioning Decision: {versioning_decision}, PublicBlock Decision: {public_access_block_decision}, MFADelete Decision: {mfa_delete_decision}')

        
class Ec2(SubCommandPlugin):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def execute(self, *args, **kwargs):
        access_key, secret_key, profile_name = get_aws_credentials()
        region = args[0]
        json_data = EC2InstanceRetriever(region=region, access_key=access_key, secret_key=secret_key).run_scan()

        if len(args) > 0 and args[0] == 'scan':
            vulernabilities_json_data = vulernabilities(json_data, "azure.nsg", "policies/azure/nsg.rego")

            return json_data, vulernabilities_json_data
        return json_data, None
    
class SecurityGroup(SubCommandPlugin):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def execute(self, *args, **kwargs):
        access_key, secret_key, profile_name = get_aws_credentials()
        region = args[0]
        json_data = AWSSecurityGroupScanner(region=region, access_key=access_key, secret_key=secret_key).run_scan()

        if len(args) > 0 and args[0] == 'scan':
            vulernabilities_json_data = vulernabilities(json_data, "azure.nsg", "policies/azure/nsg.rego")

            return json_data, vulernabilities_json_data
        return json_data, None

class RDSMySQL(SubCommandPlugin):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def execute(self, *args, **kwargs):
        access_key, secret_key, profile_name = get_aws_credentials()
        region = args[0]
        json_data = RDSMySQLDatabaseRetriever(region=region, access_key=access_key, secret_key=secret_key).run_scan()

        if len(args) > 0 and args[0] == 'scan':
            vulernabilities_json_data = vulernabilities(json_data, "obj_storage", "policies/object_storage.rego")

            return json_data, vulernabilities_json_data
        return json_data, None

class S3(SubCommandPlugin):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def execute(self, *args, **kwargs):
        access_key, secret_key, profile_name = get_aws_credentials()
        region = args[0]
        json_data = S3BucketRetriever(region=region, access_key=access_key, secret_key=secret_key).run_scan()

        if len(args) > 0 and args[0] == 'scan':
            vulernabilities_json_data = vulernabilities(json_data, "obj_storage", "policies/object_storage.rego")

            return json_data, vulernabilities_json_data
        return json_data, None
    
class AWSRootCommand(CommandPlugin):
    
    def __init__(self, *args, **kwargs):
        self.subcommands: Dict[str, Type[CommandPlugin]] = {
        "ec2": Ec2,
        "summary": Root,
        "s3" : S3,
        "security-group": SecurityGroup,
        "rds-mysql": RDSMySQL
        
    }

    def execute(self, args, *kwargs) -> any:
        region, access_key, secret_key = get_aws_credentials()
        json_data = AWSRootScanner(region=region, access_key=access_key, secret_key=secret_key).run_scan()

        if len(args) > 0 and args[0] == 'scan':
            vulernabilities_json_data = vulernabilities(json_data, "azure.nsg", "policies/azure/nsg.rego")

            return json_data, vulernabilities_json_data
        return json_data, None

    def help(self) -> str:
        return "Scans AWS."