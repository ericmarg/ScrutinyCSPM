
from typing import Protocol
import unittest
from unittest.mock import patch
from omegaconf import OmegaConf
from cli.commands.command_manager import CommandManager, CommandPlugin
from cli.commands.test_command import TestCommand


class TestCommandManager(unittest.TestCase):
    """
    A test case for the CommandManager class.
    """

    def setUp(self):
        """
        Set up the test case by creating a CommandManager instance and a configuration.
        """
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
        """
        Test the register_command method of the CommandManager class.
        """
        self.command_manager.register_command("test_command1", lambda: None)
        self.assertIn("test_command1", self.command_manager.commands)

    def test_unregister_command(self):
        """
        Test the unregister_command method of the CommandManager class.
        """
        self.command_manager.register_command("test_command", lambda: None)
        self.command_manager.unregister_command("test_command")
        self.assertNotIn("test_command", self.command_manager.commands)

    def test_execute_command(self):
        """
        Test the execute_command method of the CommandManager class.
        """
        self.command_manager.register_command("test_command1", TestCommand)
        result = self.command_manager.execute_command("test_command1", "hello", "world")
        self.assertEqual(result, "Executing MyCommand with arguments: hello, world")

    def test_execute_command_with_help(self):
        """
        Test the execute_command method of the CommandManager class with the --help argument.
        """
        self.command_manager.register_command("test_command1", TestCommand)
        result = self.command_manager.execute_command("test_command1", "--help")
        self.assertEqual(result, "Usage: test_command1 <arg1> <arg2>\nThis command concatenates arg1 and arg2 and returns the result.")

    def test_execute_nonexistent_command(self):
        """
        Test the execute_command method of the CommandManager class with a nonexistent command.
        """
        with self.assertRaises(ValueError):
            self.command_manager.execute_command("nonexistent_command")


if __name__ == "__main__":
    unittest.main