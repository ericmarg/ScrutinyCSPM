from cli.commands.command_manager import CommandPlugin

class InventoryCommand(CommandPlugin):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        arg1, arg2, arg3 = self.args
        return f"{arg1} {arg2} {arg3}"

    def help(self):
        return "Usage: inventory <arg1> <arg2> <arg3>\nThis command concatenates arg1, arg2, and arg3 and returns the result."