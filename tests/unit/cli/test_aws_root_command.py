import configparser
import json
import os
import unittest

from omegaconf import OmegaConf
from cli.commands.command_manager import CommandManager
from cli.commands.aws_root_command import AWSRootCommand
from src.scrutinycspm.resources.development.aws_root_scan import AWSRootScanner
from tests.unit.base_test_case import BaseTestCase

class TestAWSRootCommand(unittest.TestCase):
    def setUp(self):

        self.cfg = OmegaConf.create(
            {
                "commands": {
                    "inventory": {
                        "module": "commands.aws_root_command",
                        "class_name": "AWSRootCommand",
                    }
                }
            }
        )
        self.command_manager = CommandManager()
        self.command_manager.register_command(
            "aws", AWSRootCommand
        )   

    def test_awsroot_execute_command(self):
        """
        Test the execution of the Root command without any arguments.
        """
        result = self.command_manager.execute_command("aws", region="us-east-2")
        print(result)
        self.assertIsNotNone(result)


class TestAWSRootScan(BaseTestCase):
    def setUp(self):
        super().setUp(config_path="../../conf", config_name="base-config") 

    def test_aws_scan(self):

        credentials_path = self.cfg_secure.secrets.aws_credentials_file.path

        # Specify the path to the AWS credentials file
        aws_credentials_file = os.path.expanduser(credentials_path)
        config = configparser.ConfigParser()
        config.read(aws_credentials_file)
        access_key = config["default"]["aws_access_key_id"]
        secret_key = config["default"]["aws_secret_access_key"]
        region = "us-east-2"
        results = AWSRootScanner(region, access_key, secret_key).run_scan()
        print(json.dumps(results, indent=4))
        self.assertIsNotNone(results)