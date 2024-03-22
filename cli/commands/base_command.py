import argparse
from typing import Protocol

class BaseCommand(Protocol):
    cfg: dict
    args: argparse.Namespace

    def execute(self) -> None:
        ...

    def add_subparser(self, subparsers) -> None:
        ...