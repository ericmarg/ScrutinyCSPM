import argparse
import hydra
from omegaconf import DictConfig
from stevedore import driver

@hydra.main(config_path="config", config_name="conf")
def main(cfg: DictConfig) -> None:
    parser = argparse.ArgumentParser(description="ScrutinyCSPM CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    mgr = driver.DriverManager(
        namespace="cli.commands",
        name="command1",
        invoke_on_load=False,
    )

    for item in mgr.items():
        print(item)
    
    # for command_name, command_class in mgr.list_commands():
    #    command_instance = command_class(cfg, None)
    #    command_instance.add_subparser(subparsers)

    args = parser.parse_args()

    mgr = driver.DriverManager(
        namespace="cli.commands",
        name=args.command,
        invoke_on_load=True,
        invoke_args=(cfg, args),
    )
    mgr.driver.execute()

if __name__ == "__main__":
    main()