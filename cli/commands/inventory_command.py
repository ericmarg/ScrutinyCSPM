from cli.commands.command_manager import CommandPlugin
from src.scrutinycspm.utils.logging_util import add_logging

class InventoryCommand(CommandPlugin):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @add_logging
    def execute(self):
        self.log_info(f"Executing {self.__class__.__name__}")
        arg1, arg2, arg3 = self.args
        self.log_debug(f"Concatenating arg1: {arg1}, arg2: {arg2}, and arg3: {arg3}")
        return f"{arg1} {arg2} {arg3}"

    def help(self):
        return "Usage: inventory <arg1> <arg2> <arg3>\nThis command concatenates arg1, arg2, and arg3 and returns the result."