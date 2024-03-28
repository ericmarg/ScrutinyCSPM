from cli.commands.command_manager import CommandPlugin, SubCommandPlugin
from src.scrutinycspm.utils.logging_util import add_logging

class SubCommand1(SubCommandPlugin):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def execute(self, *args, **kwargs):
        if len(self.args) == 0:
            return "Executing SubCommand1"
        else:
            return f"Executing SubCommand1 with arguments: {', '.join(self.args)}"

class SubCommand2(SubCommandPlugin):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def execute(self, *args, **kwargs):
        if len(self.args) == 0:
            return "Executing SubCommand2"
        else:
            return f"Executing SubCommand2 with arguments: {', '.join(self.args)}"

class MyCommand(CommandPlugin):
    subcommands = {
        "subcommand1": SubCommand1,
        "subcommand2": SubCommand2,
    }

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