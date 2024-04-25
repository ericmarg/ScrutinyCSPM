import logging

from cli.commands.command_manager import CommandPlugin
from hydra import compose, initialize
from src.scrutinycspm.access.repository.github_provider import GitHubRepository
from hydra.core.global_hydra import GlobalHydra
from src.scrutinycspm.utils.logging_util import add_logging
from src.scrutinycspm.resources.development.aws_root_scan import AWSRootScanner
from src.scrutinycspm.utils.aws_credential_file import get_aws_credentials

class AWSRootCommand(CommandPlugin):
    """
    A command plugin for executing inventory related operations.
    """

    def __init__(self, region, *args, **kwargs):
        """
        Initialize AWS Root Inventory object.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        logging.debug("Initialized AWS Root Command")
        access_key, secret_key, profile_name = get_aws_credentials()

        logging.debug(f"Profile Name: {profile_name} found in AWS credentials file")

        self.args = args
        self.kwargs = kwargs
        self.github = None
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        GlobalHydra.instance().clear() 
        with initialize(version_base=None, config_path="../../config", job_name="aws_root_command"):
            self.cfg = compose(config_name="conf")

    @add_logging
    def execute(self, *args, **kwargs):
        """
        Execute the AWS Root Command.

        Returns:
            The result of the Root command.
        """
        self.log_info(f"Executing {self.__class__.__name__}")
        logging.debug("Calling AWSS3Command.execute")

        return self.get_inventory()

    def help(self):
        """
        Get the help message for the inventory command.

        Returns:
            The help message.
        """
        return "Usage: inventory returns the security settings from cloud providers. in this case, AWS."
    
    def get_inventory(self):
        """
        Get the inventory from the GitHub repository.

        Returns:
            The inventory from the GitHub repository.
        """
        aws_account_info = AWSRootScanner(region=self.region, access_key=self.access_key, secret_key=self.secret_key).run_scan()

        return aws_account_info