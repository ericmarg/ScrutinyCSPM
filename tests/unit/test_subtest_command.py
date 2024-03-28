import unittest
from typing import Dict, Type
from cli.commands.subtest_command import MyCommand, SubCommand1, SubCommand2
from cli.commands.command_manager import CommandManager, CommandPlugin


class TestMyCommand(unittest.TestCase):
    def setUp(self):
        self.command_manager = CommandManager()
        self.command_manager.register_command("mycommand", MyCommand)

    def test_execute_command(self):
        result = self.command_manager.execute_command("mycommand")
        self.assertEqual(result, "Executing MyCommand")

    def test_execute_command_with_args(self):
        result = self.command_manager.execute_command("mycommand", "arg1", "arg2")
        self.assertEqual(result, "Executing MyCommand with arguments: arg1, arg2")

    def test_execute_subcommand1(self):
        result = self.command_manager.execute_command("mycommand", "subcommand1")
        self.assertEqual(result, "Executing SubCommand1")

    def test_execute_subcommand2(self):
        result = self.command_manager.execute_command("mycommand", "subcommand2")
        self.assertEqual(result, "Executing SubCommand2")

    def test_unknown_command(self):
        with self.assertRaises(ValueError):
            self.command_manager.execute_command("unknowncommand")

    def test_unknown_subcommand(self):
        
        self.command_manager.execute_command("mycommand", "unknownsubcommand")

if __name__ == '__main__':
    unittest.main()