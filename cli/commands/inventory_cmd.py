import argparse
from stevedore import driver

class InventoryCmd:
    def __init__(self, cfg, args):
        self.cfg = cfg
        self.args = args

    def execute(self):
        subcommand = self.args.subcommand
        mgr = driver.DriverManager(
            namespace=f"scrutinycspm.cli.commands.InventoryCmd.{subcommand}",
            name=subcommand,
            invoke_on_load=True,
            invoke_args=(self.cfg, self.args),
        )
        mgr.driver.execute()

    def add_subparser(self, subparsers):
        parser_inventory = subparsers.add_parser("inventory", help="Inventory Command help")
        subparsers_provider = parser_inventory.add_subparsers(dest="subcommand", required=True)
        subparsers_provider.add_parser("provider", help="Provider Command help")
        #subparsers_provider.add_parser("subcommand2", help="Subcommand 2")