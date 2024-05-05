import configparser
import os

from hydra.core.global_hydra import GlobalHydra
import json
import os
from src.scrutinycspm.resources.development.ansible_scanning.aws_s3_bucket_ansible_scan import AWSS3Scanner
from src.scrutinycspm.resources.development.bridges.execute_bucket_info import transformation

from tests.unit.base_test_case import BaseTestCase

class TestAwsS3AnsibleScan(BaseTestCase):
    def setUp(self):
        super().setUp(config_path="../../conf", config_name="base-config") 

    def test_s3_ansible_scan(self):

        credentials_path = self.cfg_secure.secrets.aws_credentials_file.path
                
        ansible_test = bool(self.cfg.ansible.unit_testing)

        if ansible_test:    
            # Specify the path to the AWS credentials file
            aws_credentials_file = os.path.expanduser(credentials_path)
            config = configparser.ConfigParser()
            config.read(aws_credentials_file)
            access_key = config["default"]["aws_access_key_id"]
            secret_key = config["default"]["aws_secret_access_key"]
            region = "us-east-2"
            raw_s3_results, rego_policy_content = AWSS3Scanner(region, access_key, secret_key).run_scan()
            print(json.dumps(raw_s3_results, indent=4))
            self.assertIsNotNone(raw_s3_results)

            print("\nRego Policy Content\n\n")
            print(json.dumps(rego_policy_content, indent=4))
            self.assertIsNotNone(rego_policy_content)
        else:
            assert True
            
    def test_s3_ansible_transformation(self):

        credentials_path = self.cfg_secure.secrets.aws_credentials_file.path

        # Specify the path to the AWS credentials file
        aws_credentials_file = os.path.expanduser(credentials_path)
        config = configparser.ConfigParser()
        config.read(aws_credentials_file)
        access_key = config["default"]["aws_access_key_id"]
        secret_key = config["default"]["aws_secret_access_key"]
        region = "us-east-2"
        raw_s3_results, rego_policy_content = AWSS3Scanner(region, access_key, secret_key).run_scan()
        print(json.dumps(raw_s3_results, indent=4))
        self.assertIsNotNone(raw_s3_results)

        print("\nRego Policy Content\n\n")
        print(json.dumps(rego_policy_content, indent=4))
        self.assertIsNotNone(rego_policy_content)


        print("\Transformed Results Content\n\n")
        # Transform the raw results into a format that can be used by the Rego policy
        transformed_results = transformation(raw_s3_results)
        print(json.dumps(transformed_results, indent=4))
        self.assertIsNotNone(transformed_results)

