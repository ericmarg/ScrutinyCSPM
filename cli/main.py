# cli/main.py
import argparse
import hydra
from omegaconf import DictConfig
from stevedore import driver

@hydra.main(config_path="config", config_name="config")
def main(cfg: DictConfig) -> None:
    parser = argparse.ArgumentParser(description="ScrutinyCSPM CLI")
    
    # Add command line arguments
    parser.add_argument("command", help="The command to execute")
    parser.add_argument("--param1", type=str, help="Parameter 1")
    parser.add_argument("--param2", type=int, default=0, help="Parameter 2")
    
    # Parse the command line arguments
    args = parser.parse_args()
    
    # Use Stevedore to load and execute the appropriate command plugin
    mgr = driver.DriverManager(
        namespace="scrutinycspm.cli.commands",
        name=args.command,
        invoke_on_load=True,
        invoke_args=(cfg, args),
    )
    
    # Execute the command
    mgr.driver.execute()

if __name__ == "__main__":
    main()