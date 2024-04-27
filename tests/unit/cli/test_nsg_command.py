import configparser
import json
import os
import unittest

from omegaconf import OmegaConf
from cli.commands.azure_root_command import AzureRootCommand
from cli.commands.command_manager import CommandManager

from tests.unit.base_test_case import BaseTestCase

class TestAzureNSGCommand(unittest.TestCase):
    def setUp(self):

        self.cfg = OmegaConf.create(
            {
                "commands": {
                    "inventory": {
                        "module": "commands.azure_nsg_command",
                        "class_name": "AzureRootCommand",
                    }
                }
            }
        )
        self.command_manager = CommandManager()
        self.command_manager.register_command("azure", AzureRootCommand)

    def test_azurensg_execute_command(self):
        """
        Test the execution of the Root command without any arguments.
        """
        result = self.command_manager.execute_command("azure", "nsg")
        print(result)
        self.assertIsNotNone(result)


