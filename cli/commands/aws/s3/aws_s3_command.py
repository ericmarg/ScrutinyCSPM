
import logging
from cli.commands.command_manager import CommandPlugin
from hydra import compose, initialize
from src.scrutinycspm.access.repository.github_provider import GitHubRepository
from hydra.core.global_hydra import GlobalHydra
from src.scrutinycspm.utils.logging_util import add_logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class AWSS3Command(CommandPlugin):
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
        logging.debug("Initialized AWS S3 Command")
        self.args = args
        self.kwargs = kwargs
        self.github = None
        GlobalHydra.instance().clear() 
        with initialize(version_base=None, config_path="../../../config", job_name="aws_s3_command"):
            self.cfg = compose(config_name="conf")

    @add_logging
    def execute(self):
        """
        Execute the S3 Main Commands.

        Returns:
            The result of the inventory command.
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
        return "Getting inventory from AWS S3"