
from typing import Callable, Protocol

from src.scrutinycspm.utils.logging_util import add_logging
from typing import Protocol, Type, Dict

class SubCommandPlugin(Protocol):
    def execute(self, *args, **kwargs):
        ...

    def help(self) -> str:
        ...
@add_logging
class CommandPlugin(Protocol):

    def execute(self, *args, **kwargs) -> any:
        ...
    def help(self) -> str:
        ...


class CommandManager:
    def __init__(self):
        self.commands: Dict[str, Type[CommandPlugin]] = {}

    def register_command(self, name: str, command_class: Type[CommandPlugin]):
        self.commands[name] = command_class

    def unregister_command(self, name: str):
        del self.commands[name]

    def execute_command(self, name: str, *args, **kwargs):
        if name not in self.commands:
            raise ValueError(f"Unknown command: {name}")

        command_class = self.commands[name]
        command = command_class(*args, **kwargs)

        if len(args) > 0 and args[0] in command.subcommands:
            subcommand_name = args[0]
            subcommand_args = args[1:]
            subcommand_class = command.subcommands[subcommand_name]
            subcommand = subcommand_class(*subcommand_args, **kwargs)
            return subcommand.execute()
        else:
            return command.execute(*args, **kwargs)