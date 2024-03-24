from cli.commands.command_manager import CommandPlugin
from src.scrutinycspm.utils.logging_util import add_logging

@add_logging
class TestCommand(CommandPlugin):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        self.log_debug(f"Executing {self.__class__.__name__}")
        arg1, arg2 = self.args
        self.log_debug(f"Concatenating arg1: {arg1} and arg2: {arg2}")
        return f"{arg1} {arg2}"

    def help(self):
        return "Usage: test_command1 <arg1> <arg2>\nThis command concatenates arg1 and arg2 and returns the result."