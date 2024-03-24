import argparse
import json
from dataclasses import dataclass
import hydra
from omegaconf import DictConfig
from typing import Any, Dict
from cli.commands.command_manager import CommandManager

import logging
import importlib

@hydra.main(config_path="config", config_name="conf")
def main(cfg: DictConfig) -> None:
    parser = argparse.ArgumentParser(description="ScrutinyCSPM CLI")
    parser.add_argument("command", nargs="?", help="The command to execute")
    parser.add_argument("args", nargs="*", help="Additional arguments for the command")

    # Parse the command-line arguments
    args = parser.parse_args()

    command_manager = CommandManager()

    # Load command plugins dynamically based on the Hydra configuration
    for command_name, command_config in cfg.commands.items():
        module = importlib.import_module(command_config.module)
        command_class = getattr(module, command_config.class_name)
        command_manager.register_command(command_name, command_class)

    # Check if a command is provided
    if args.command:
        command_name = args.command
        command_args = args.args

        try:
            return command_manager.execute_command(command_name, *command_args)
        except ValueError as e:
            print(f"Error: {str(e)}")
            print("Available commands:")
            for cmd in command_manager.commands:
                print(f"- {cmd}")
    else:
        # No command provided, display available commands
        print("Available commands:")
        for cmd in command_manager.commands:
            print(f"- {cmd}")


if __name__ == "__main__":
    main()