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

    command_manager = CommandManager()

    for command_name, command_config in cfg.commands.items():
        module = importlib.import_module(command_config.module)
        command_class = getattr(module, command_config.class_name)
        command_manager.register_command(command_name, command_class)

    # Execute commands
    command_manager.execute_command("inventory", "arg1", "arg2", kwarg1="value1")
    command_manager.execute_command("certificate", "arg3", kwarg2="value2")




if __name__ == "__main__":
    main()