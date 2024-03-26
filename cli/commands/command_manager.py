import importlib
import inspect
from typing import Callable, Protocol
import sys

from src.scrutinycspm.utils.logging_util import add_logging


@add_logging
class CommandPlugin(Protocol):

    def execute(self, *args, **kwargs) -> any:
        ...
    def help(self) -> str:
        ...


class CommandManager:
    """
    A class that manages commands for the CLI application.
    """

    def __init__(self):
        self.commands = {}

    def register_command(self, name: str, command_class: Callable[..., CommandPlugin]):
        """
        Registers a command with the given name and command class.

        Args:
            name (str): The name of the command.
            command_class (Callable[..., CommandPlugin]): The command class.

        Returns:
            None
        """
        self.commands[name] = command_class

    def unregister_command(self, name: str):
        """
        Unregisters a command with the given name.

        Args:
            name (str): The name of the command.

        Returns:
            None
        """
        self.commands.pop(name, None)

    def execute_command(self, name: str, *args, **kwargs):
        """
        Executes a command with the given name and arguments.

        Args:
            name (str): The name of the command.
            *args: Variable length arguments.
            **kwargs: Keyword arguments.

        Returns:
            The result of the command execution.
        """
        if name not in self.commands:
            raise ValueError(f"Command '{name}' not found.")

        command_class = self.commands[name]

        if "--help" in args:
            command = command_class()
            return command.help()

        command = command_class(*args, **kwargs)
        return command.execute()