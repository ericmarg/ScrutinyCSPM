import argparse
from typing import Protocol
import unittest
from unittest.mock import patch
from omegaconf import OmegaConf
from cli.commands.command_manager import CommandManager

import cli.main as main


class CommandPlugin(Protocol):
    def execute(self, *args, **kwargs) -> None:
        ...

class TestCommandManager(unittest.TestCase):
    def setUp(self):
        self.command_manager = CommandManager()
        self.cfg = OmegaConf.create({
            "commands": {
                "test_command1": {
                    "module": "test_module1",
                    "class_name": "TestCommand1"
                },
                "test_command2": {
                    "module": "test_module2",
                    "class_name": "TestCommand2"
                }
            }
        })

    def test_register_command(self):
        self.command_manager.register_command("test_command1", lambda: None)
        self.assertIn("test_command1", self.command_manager.commands)

    def test_unregister_command(self):
        self.command_manager.register_command("test_command", lambda: None)
        self.command_manager.unregister_command("test_command")
        self.assertNotIn("test_command", self.command_manager.commands)

    def test_execute_command(self):
        def test_command(arg1, arg2):
            return f"{arg1} {arg2}"

        self.command_manager.register_command("test_command1", test_command)
        result = self.command_manager.execute_command("test_command1", "hello", "world")
        self.assertEqual(result, "hello world")

    def test_execute_nonexistent_command(self):
        with self.assertRaises(ValueError):
            self.command_manager.execute_command("nonexistent_command")

    
if __name__ == "__main__":
    unittest.main