import logging
import os
from typing import Dict, Type
import json

from cli.commands.command_manager import CommandPlugin, SubCommandPlugin
from cli.commands.aws.rds.aws_rds_mysql_subcmd import RDSMySQL
from hydra import compose, initialize
from src.scrutinycspm.access.repository.github_provider import GitHubRepository
from hydra.core.global_hydra import GlobalHydra
from src.scrutinycspm.providers.azure.policy_check import vulernabilities
from src.scrutinycspm.resources.development.aws_ec2_scan import EC2InstanceRetriever
from src.scrutinycspm.resources.development.aws_s3bucket_scan import S3BucketRetriever
from src.scrutinycspm.resources.development.aws_security_group_scan import (
    AWSSecurityGroupScanner,
)
from src.scrutinycspm.utils.args import is_arg_present
from src.scrutinycspm.utils.logging_util import add_logging
from src.scrutinycspm.resources.development.aws_root_scan import AWSRootScanner
from cli.commands.bridges.aws.s3_bridge import (evaluate_object_storage_containers, s3_transformation)
from src.scrutinycspm.utils.aws_credential_file import get_aws_credentials
from opa_client.opa import OpaClient
from opa_client.errors import ConnectionsError
from src.scrutinycspm.utils.region import find_aws_region
from typing import Type

from cli.commands.command_manager import SubCommandPlugin
from src.scrutinycspm.providers.azure.policy_check import vulernabilities
from src.scrutinycspm.utils.aws_credential_file import get_aws_credentials


class Root(SubCommandPlugin):
    """
    Subcommand class for the 'summary' command.
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def execute(self, *args, **kwargs):
        """
        Executes the 'summary' command.
        """
        access_key, secret_key, profile = get_aws_credentials()
        region = find_aws_region(args)

        json_data = AWSRootScanner(
            region=region, access_key=access_key, secret_key=secret_key
        ).run_scan()

        data = json.loads(json_data)
        json_data = json.dumps(data, indent=4, sort_keys=True)

        print(json_data)

        if is_arg_present(args=args, arg_value="scan"):
            vulernabilities_json_data = vulernabilities(
                json_data, "azure.nsg", "policies/azure/nsg.rego"
            )

            return json_data, vulernabilities_json_data
        return "Command completed!", None


class Ec2(SubCommandPlugin):
    """
    Subcommand class for the 'ec2' command.
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def execute(self, *args, **kwargs):
        """
        Executes the 'ec2' command.
        """
        access_key, secret_key, profile_name = get_aws_credentials()
        region = args[0]
        json_data = EC2InstanceRetriever(
            region=region, access_key=access_key, secret_key=secret_key
        ).run_scan()

        data = json.loads(json_data)
        json_data = json.dumps(data, indent=4, sort_keys=True)
        print(json_data)

        if len(args) > 0 and args[0] == "scan":
            vulernabilities_json_data = vulernabilities(
                json_data, "azure.nsg", "policies/azure/nsg.rego"
            )

            return json_data, vulernabilities_json_data
        return "Command completed!", None


class SecurityGroup(SubCommandPlugin):
    """
    Subcommand class for the 'security-group' command.
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def execute(self, *args, **kwargs):
        """
        Executes the 'security-group' command.
        """
        access_key, secret_key, profile_name = get_aws_credentials()
        region = find_aws_region(args)
        json_data = AWSSecurityGroupScanner(
            region=region, access_key=access_key, secret_key=secret_key
        ).run_scan()

        data = json.loads(json_data)
        json_data = json.dumps(data, indent=4, sort_keys=True)
        print(json_data)

        if is_arg_present(args=args, arg_value="scan"):
            vulernabilities_json_data = vulernabilities(
                json_data, "azure.nsg", "policies/azure/nsg.rego"
            )

            return json_data, vulernabilities_json_data
        return "Command completed!", None


class S3(SubCommandPlugin):
    """
    Subcommand class for the 's3' command.
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def execute(self, *args, **kwargs):
        """
        Executes the 's3' command.
        """
        access_key, secret_key, profile_name = get_aws_credentials()
        region = find_aws_region(args)

        if region is None:
            return "Region not found", None

        print(f"Retrieving S3 buckets, region: {region}...")
        json_data = S3BucketRetriever(
            region=region, access_key=access_key, secret_key=secret_key
        ).run_scan()

        if is_arg_present(args=args, arg_value="github"):
            github = GitHubRepository('robertfischer3/scrutiny-policies')
            policies = github.get_files_by_extension('storage', '.rego')
            for policy in policies:
                print(f"Policy group retrieved: {policy}")
                policy_content = github.get_file_contents(policy, 'main')
                print(policy_content)

        AWSRootCommand.process_data_internal(
            self,
            json_data,
            args,
            region,
            s3_transformation,
            evaluate_object_storage_containers,
            policy_file_path="policies/object_storage.rego",
            endpoint="obj_storage",
        )


class AWSRootCommand(CommandPlugin):
    """
    Command class for the 'aws-root' command.
    """

    def __init__(self, *args, **kwargs):
        self.subcommands: Dict[str, Type[CommandPlugin]] = {
            "ec2": Ec2,
            "summary": Root,
            "s3": S3,
            "security-group": SecurityGroup,
            "rds-mysql": RDSMySQL,
        }

    def execute(self, args, *kwargs) -> any:
        """
        Executes the 'aws-root' command.
        """
        region, access_key, secret_key = get_aws_credentials()
        json_data = AWSRootScanner(
            region=region, access_key=access_key, secret_key=secret_key
        ).run_scan()

        if len(args) > 0 and args[0] == "scan":
            vulernabilities_json_data = vulernabilities(
                json_data, "azure.nsg", "policies/azure/nsg.rego"
            )

            return json_data, vulernabilities_json_data
        return json_data, None

    def help(self) -> str:
        """
        Returns the help message for the 'aws-root' command.
        """
        return "Scans AWS."

    @staticmethod
    def process_data_internal(
        self,
        json_data,
        args,
        region,
        transforming_function,
        processing_function,
        **kwargs,
    ):
        """
        Processes the data returned by the scan.
        """
        data = json.loads(json_data)
        json_data = json.dumps(data, indent=4, sort_keys=True)
            
        if is_arg_present(args=args, arg_value="region"):
            print("Please specify a region")
            return None, None


        if is_arg_present(args=args, arg_value="scan"):
            if transforming_function:
                resource_dict = transforming_function(json_data)
            else:
                raise ValueError("Transformation function not found")

            if processing_function:
                if kwargs.get("policy"):
                    with open(kwargs.get("policy"), "r") as file:
                        policy = file.read()
                        endpoint = kwargs.get("endpoint")
                        processing_function(
                            resource_dict, policy=policy, endpoint=endpoint
                        )
                if kwargs.get("policy_file_path"):
                        endpoint = kwargs.get("endpoint")
                        processing_function(
                            resource_dict, policy_file_path=kwargs.get("policy_file_path"), endpoint=endpoint)
            
            else:
                raise ValueError("Processing function not found")

        if is_arg_present(args=args, arg_value="verbose"):
            print(json_data)

        if is_arg_present(args=args, arg_value="raw"):
            return json_data, None

        return "Scan completed", None

    @staticmethod
    def process_data_github(
        self,
        json_data,
        args,
        region,
        transforming_function,
        processing_function,
        **kwargs,
    ):
        """
        Processes the data returned by the scan.
        """
        data = json.loads(json_data)
        json_data = json.dumps(data, indent=4, sort_keys=True)

        if len(args) == 1 and args[0] == region:
            print(json_data)
            return None, None

        if is_arg_present(args=args, arg_value="scan"):
            if transforming_function:
                s3_dict = transforming_function(json_data)
            else:
                raise ValueError("Transformation function not found")

            if processing_function:
                with open(kwargs.get("file_path"), "r") as file:
                    policy_file = file.read()
                    endpoint = kwargs.get("endpoint")
                    processing_function(
                        s3_dict, policy_file=policy_file, endpoint=endpoint
                    )

            else:
                raise ValueError("Processing function not found")

        if is_arg_present(args=args, arg_value="verbose"):
            print(json_data)

        if is_arg_present(args=args, arg_value="raw"):
            return json_data, None

        return "Scan completed", None
