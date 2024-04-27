
import hydra
from omegaconf import DictConfig
from typing import Any, Dict
from commands.command_manager import CommandManager
import logging
import importlib
import argparse

@hydra.main(config_path="config", config_name="conf", version_base=None)
def main(cfg: DictConfig) -> None:
    logging.basicConfig(level=cfg.logging.level, filename="app.log")

    print("Welcome to Scrutiny CSPM CLI")

    command_manager = CommandManager()

    # Load command plugins dynamically based on the Hydra configuration
    for command_name, command_config in cfg.commands.items():
        module = importlib.import_module(command_config.module)
        command_class = getattr(module, command_config.class_name)
        command_manager.register_command(command_name, command_class)

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Scrutiny CSPM CLI")
    parser.add_argument("command", nargs='?', help="Command to execute (leave blank for interactive mode)")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments for the command")
    args = parser.parse_args()

    # Determine execution mode based on the command input
    if args.command:
        if args.command == 'quit':
            print("Exiting...")
            return

        try:
            result = command_manager.execute_command(args.command, *args.args)
            if result is not None:
                print(result)
        except ValueError as e:
            print(f"Error: {str(e)}")
            print("Available commands:")
            for cmd in command_manager.commands:
                print(f"- {cmd}")
    else:
        # Enter interactive mode
        while True:
            command_input = input("Enter a command (or 'quit' to exit): ")
            if command_input.lower() == "quit":
                print("Exiting...")
                break

            command_parts = command_input.split()
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
