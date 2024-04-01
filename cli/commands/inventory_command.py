from hydra import compose, initialize
from omegaconf import DictConfig, OmegaConf
from cli.commands.command_manager import CommandPlugin
from src.scrutinycspm.utils.logging_util import add_logging
from src.scrutinycspm.providers.aws.resources.account import AWSAccount
from opa_client.opa import OpaClient
from opa_client.errors import ConnectionsError
import logging
from src.scrutinycspm.access.repository.github_provider import GitHubRepository
import os

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class InventoryCommand(CommandPlugin):
    def __init__(self, *args, **kwargs):
        logging.debug("Initialized InventoryCommand")
        self.args = args
        self.kwargs = kwargs
        with initialize(version_base=None, config_path="../config", job_name="inventory_command"):
            self.cfg = compose(config_name="conf")

        

    @add_logging
    def execute(self):
        self.log_info(f"Executing {self.__class__.__name__}")
        logging.debug("Calling InventoryCommand.execute")

        return self.get_inventory()

    def help(self):
        return "Usage: inventory returns the result."
    


    def get_policies(self): 
        
        if self.cfg is not None:
            github = GitHubRepository(self.cfg.policies.policy_repo)
            policies = github.get_files_by_extension(self.cfg.policies.path, ".rego")
            return policies
    


    def get_inventory(self):

        aws = AWSAccount()
        opa = OpaClient()

        for container in aws.obj_storage_containers:
            self.format_output(container)

            container_dict = container.to_dict()
            try:
                
                opa.update_opa_policy_fromfile(
                    filepath="policies/object_storage.rego", endpoint="obj_storage"
                )
                opa_result = opa.check_policy_rule(
                    input_data=container_dict,
                    package_path="obj_storage",
                    rule_name="obj_storage_container_compliant",
                )
                print(
                    f"Object Storage Container: {container.name}, Compliant: {opa_result}"
                )
            except ConnectionsError:
                print(
                    "OPA Server Unreachable, please check to make sure OPA server is running."
                )

        return aws

    def format_output(self, container):
        print(
            f"Name: {container.name}, PublicAccessBlocked: {container.all_public_access_blocked}, Region: {container.region}, VersioningEnabled: {container.versioning_enabled}"
        )
