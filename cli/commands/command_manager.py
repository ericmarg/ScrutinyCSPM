import importlib
import inspect
from typing import Callable, Protocol
from src.scrutinycspm.utils.logging_util import add_logging

@add_logging
class CommandPlugin(Protocol):

    def execute(self, *args, **kwargs) -> any:
        ...
    def help(self) -> str:
        ...


class CommandManager:
    def __init__(self):
        self.commands = {}

    def register_command(self, name: str, command_class: Callable[..., CommandPlugin]):
        self.commands[name] = command_class

    def unregister_command(self, name: str):
        self.commands.pop(name, None)

    def execute_command(self, name: str, *args, **kwargs):
        if name not in self.commands:
            raise ValueError(f"Command '{name}' not found.")

        command_class = self.commands[name]

        if "--help" in args:
            command = command_class()
            return command.help()


        command = command_class(*args, **kwargs)
        return command.execute()