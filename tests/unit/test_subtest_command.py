import unittest
from typing import Dict, Type
from cli.commands.subcommand_example_command import MySubCommand
from cli.commands.command_manager import CommandManager


import unittest

class TestMyCommand(unittest.TestCase):
    """
    A test case for the MyCommand class.
    """

    def setUp(self):
        """
        Set up the test case by creating a CommandManager instance and registering the MyCommand command.
        """
        self.command_manager = CommandManager()
        self.command_manager.register_command("mycommand", MySubCommand)

    def test_execute_command(self):
        """
        Test the execution of the MyCommand command without any arguments.
        """
        result = self.command_manager.execute_command("mycommand")
        self.assertEqual(result, "Executing MyCommand")

    def test_execute_command_with_args(self):
        """
        Test the execution of the MyCommand command with arguments.
        """
        result = self.command_manager.execute_command("mycommand", "arg1", "arg2")
        self.assertEqual(result, "Executing MyCommand with arguments: arg1, arg2")

    def test_execute_subcommand1(self):
        """
        Test the execution of the SubCommand1 subcommand of the MyCommand command.
        """
        result = self.command_manager.execute_command("mycommand", "subcommand1")
        self.assertEqual(result, "Executing SubCommand1")

    def test_execute_subcommand2(self):
        """
        Test the execution of the SubCommand2 subcommand of the MyCommand command.
        """
        result = self.command_manager.execute_command("mycommand", "subcommand2")
        self.assertEqual(result, "Executing SubCommand2")

    def test_unknown_command(self):
        """
        Test the execution of an unknown command, which should raise a ValueError.
        """
        with self.assertRaises(ValueError):
            self.command_manager.execute_command("unknowncommand")

    def test_unknown_subcommand(self):
        """
        Test the execution of an unknown subcommand of the MyCommand command, which should raise a ValueError.
        """
        self.command_manager.execute_command("mycommand", "unknownsubcommand")

if __name__ == '__main__':
    unittest.main()