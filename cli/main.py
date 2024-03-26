from dataclasses import dataclass
import hydra
from omegaconf import DictConfig
from typing import Any, Dict
from commands.command_manager import CommandManager
import logging
import importlib


@hydra.main(config_path="config", config_name="conf", version_base=None)
def main(cfg: DictConfig) -> None:
    logging.basicConfig(level=cfg.logging.level, filename="app.log")
    
    print("Welcome to Scrutiny CSP CLI")
    
    command_manager = CommandManager()

    # Load command plugins dynamically based on the Hydra configuration
    for command_name, command_config in cfg.commands.items():
        module = importlib.import_module(command_config.module)
        command_class = getattr(module, command_config.class_name)
        command_manager.register_command(command_name, command_class)

    while True:
        command = input("Enter a command (or 'quit' to exit): ")

        if command.lower() == "quit":
            print("Exiting...")
            break

        command_parts = command.split()
        command_name = command_parts[0]
        command_args = command_parts[1:]

        try:
            result = command_manager.execute_command(command_name, *command_args)
            if result is not None:
                print(result)
        except ValueError as e:
            print(f"Error: {str(e)}")
            print("Available commands:")
            for cmd in command_manager.commands:
                print(f"- {cmd}")


if __name__ == "__main__":
    main()
