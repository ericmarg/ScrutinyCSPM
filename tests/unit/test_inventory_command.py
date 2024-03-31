import unittest
from typing import Dict, Type
from cli.commands.inventory_command import InventoryCommand
from cli.commands.command_manager import CommandManager
from hydra.core.global_hydra import GlobalHydra
import hydra


class TestInventoryCommand(unittest.TestCase):
    def setUp(self):
        
        GlobalHydra.instance().clear()

        hydra.initialize(
            config_path="/cli/config/conf.yaml", job_name="test_job", version_base="1.1"
        )
        self.cfg = hydra.compose(config_name="commands")
        self.command_manager = CommandManager()

    def test_execute_command(self):
        """
        Test the execution of the MyCommand command without any arguments.
        """
        result = self.command_manager.execute_command("inventory")
        self.assertEqual(result, "Executing inventory")