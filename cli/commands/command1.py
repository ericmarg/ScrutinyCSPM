import argparse
from stevedore import driver

class Command1:
    def __init__(self, cfg, args):
        self.cfg = cfg
        self.args = args

    def execute(self):
        subcommand = self.args.subcommand
        mgr = driver.DriverManager(
            namespace=f"scrutinycspm.cli.commands.command1.{subcommand}",
            name=subcommand,
            invoke_on_load=True,
            invoke_args=(self.cfg, self.args),
        )
        mgr.driver.execute()

    def add_subparser(self, subparsers):
        parser_command1 = subparsers.add_parser("command1", help="Command 1")
        subparsers_command1 = parser_command1.add_subparsers(dest="subcommand", required=True)
        subparsers_command1.add_parser("subcommand1", help="Subcommand 1")
        subparsers_command1.add_parser("subcommand2", help="Subcommand 2")