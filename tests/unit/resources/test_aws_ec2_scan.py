import configparser
import os

from src.scrutinycspm.resources.development.ansible_scanning.aws_ec2_ansible_scan import AWSEC2Scanner
from hydra.core.global_hydra import GlobalHydra
import json
import os

from tests.unit.base_test_case import BaseTestCase

class TestAWSEc2AnsibleScan(BaseTestCase):
    def setUp(self):
        super().setUp(config_path="../../conf", config_name="base-config") 

    def test_ec2_scan(self):

        credentials_path = self.cfg_secure.secrets.aws_credentials_file.path

        # Specify the path to the AWS credentials file
        aws_credentials_file = os.path.expanduser(credentials_path)
        config = configparser.ConfigParser()
        config.read(aws_credentials_file)
        access_key = config["default"]["aws_access_key_id"]
        secret_key = config["default"]["aws_secret_access_key"]
        region = "us-east-2"
        results = AWSEC2Scanner(region, access_key, secret_key).run_scan()
        print(json.dumps(results, indent=4))
        self.assertIsNotNone(results)

