import unittest

from omegaconf import OmegaConf
from cli.commands.inventory_command import InventoryCommand
from cli.commands.command_manager import CommandManager
from hydra.core.global_hydra import GlobalHydra
import hydra


class TestInventoryCommand(unittest.TestCase):
    def setUp(self):

        self.cfg = OmegaConf.create(
            {
                "commands": {
                    "inventory": {
                        "module": "commands.inventory_command",
                        "class_name": "InventoryCommand",
                    }
                }
            }
        )
        self.command_manager = CommandManager()
        self.command_manager.register_command(
            "inventory", InventoryCommand
        )   

    def test_execute_command(self):
        """
        Test the execution of the Inventory command without any arguments.
        """
        result = self.command_manager.execute_command("inventory")
        self.assertIsNotNone(result)

    def test_execute_command_wo_args(self):
        """
        Test the execution of the Inventory command without any arguments.
        """
        result = self.command_manager.execute_command("inventory")
        self.assertIsNotNone(result)