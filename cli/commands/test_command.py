from cli.commands.command_manager import CommandPlugin
from src.scrutinycspm.utils.logging_util import add_logging

@add_logging
class TestCommand(CommandPlugin):
    subcommands = {}

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @add_logging
    def execute(self, *args, **kwargs):
        self.log_debug(f"Executing {self.__class__.__name__}")
        if len(self.args) == 0:
            return "Executing MyCommand"
        else:
            return f"Executing MyCommand with arguments: {', '.join(self.args)}"

    def help(self):
        return "Usage: test_command1 <arg1> <arg2>\nThis command concatenates arg1 and arg2 and returns the result."