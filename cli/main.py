import argparse
import json
from dataclasses import dataclass
import hydra
from omegaconf import DictConfig
from typing import Any, Dict
from cli.commands.command_manager import CommandManager
from cli.commands.inventory_command import InventoryCommand
from cli.commands.certificate_command import CertificateCommand
import logging
import importlib

@hydra.main(config_path="config", config_name="conf")
def main(cfg: DictConfig) -> None:
    parser = argparse.ArgumentParser(description="ScrutinyCSPM CLI")

    command_manager = CommandManager()
    
    certificate_module = importlib.import_module("commands.certificate_command")
    inventory_module = importlib.import_module("commands.inventory_command")

    # Register command plugins
    command_manager.register_command("inventory", inventory_module.InventoryCommand)
    command_manager.register_command("certificate", certificate_module.CertificateCommand)

    # Execute commands
    command_manager.execute_command("inventory", "arg1", "arg2", kwarg1="value1")
    command_manager.execute_command("certificate", "arg3", kwarg2="value2")

    # Unregister a command
    command_manager.unregister_command("inventory")

    # Try executing the unregistered command (raises ValueError)
    command_manager.execute_command("inventory")


if __name__ == "__main__":
    main()