import configparser
import os

from src.scrutinycspm.resources.development.aws_rds_scan import RDSMySQLDatabaseRetriever
from hydra.core.global_hydra import GlobalHydra
import json
import os

from tests.unit.base_test_case import BaseTestCase

class TestAWSRDSScan(BaseTestCase):
    def setUp(self):
        super().setUp(config_path="../../conf", config_name="base-config") 

    def test_rds_scan(self):

        credentials_path = self.cfg_secure.secrets.aws_credentials_file.path

        # Specify the path to the AWS credentials file
        aws_credentials_file = os.path.expanduser(credentials_path)
        config = configparser.ConfigParser()
        config.read(aws_credentials_file)
        access_key = config["default"]["aws_access_key_id"]
        secret_key = config["default"]["aws_secret_access_key"]
        region = "us-east-2"
        results = RDSMySQLDatabaseRetriever(access_key, secret_key, region).run_scan()
        print(json.dumps(results, indent=4))
        self.assertIsNotNone(results)

