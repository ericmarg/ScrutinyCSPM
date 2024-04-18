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
from hydra.core.global_hydra import GlobalHydra

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class InventoryCommand(CommandPlugin):
    """
    A command plugin for executing inventory related operations.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the InventoryCommand object.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        logging.debug("Initialized InventoryCommand")
        self.args = args
        self.kwargs = kwargs
        self.github = None
        GlobalHydra.instance().clear() 
        with initialize(version_base=None, config_path="../config", job_name="inventory_command"):
            self.cfg = compose(config_name="conf")

    @add_logging
    def execute(self):
        """
        Execute the inventory command.

        Returns:
            The result of the inventory command.
        """
        self.log_info(f"Executing {self.__class__.__name__}")
        logging.debug("Calling InventoryCommand.execute")

        return self.get_inventory()

    def help(self):
        """
        Get the help message for the inventory command.

        Returns:
            The help message.
        """
        return "Usage: inventory returns the security settings from cloud providers. in this case, AWS."

    def get_policies(self):
        """
        Get the policies from the GitHub repository.

        Returns:
            The policies from the GitHub repository.
        """
        if self.cfg is not None:
            self.github = GitHubRepository(self.cfg.policy.github.repository)
            policies = self.github.get_files_by_extension(self.cfg.policy.github.path, ".rego")
            return policies

    def get_inventory(self):
        """
        Get the inventory.

        Returns:
            The inventory.
        """
        policies = self.get_policies()

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
        """
        Format the output for a container.

        Args:
            container: The container to format the output for.
        """
        print(
            f"Name: {container.name}, PublicAccessBlocked: {container.all_public_access_blocked}, VersioningEnabled: {container.versioning_enabled}"
        )
