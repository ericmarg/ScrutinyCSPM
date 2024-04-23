import logging
from command_manager import CommandPlugin, SubCommandPlugin
from hydra import compose, initialize

class Inventory(SubCommandPlugin):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def execute(self, *args, **kwargs):
        if len(self.args) == 0:
            return "Executing AWS Inventory"
        else:
            return f"Executing SubCommand1 with arguments: {', '.join(self.args)}"
