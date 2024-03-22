import importlib
import inspect
from typing import Callable, Protocol


class CommandPlugin(Protocol):
    def execute(self, *args, **kwargs) -> None:
        ...


class CommandManager:
    def __init__(self):
        self.commands = {}

    def register_command(self, name: str, command_class: Callable[..., CommandPlugin]):
        self.commands[name] = command_class

    def unregister_command(self, name: str):
        self.commands.pop(name, None)

    def execute_command(self, name: str, *args, **kwargs):
        command_class = self.commands.get(name)
        if command_class:
            command = command_class()
            command.execute(*args, **kwargs)
        else:
            raise ValueError(f"Command '{name}' not found.")