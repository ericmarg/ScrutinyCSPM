import configparser
from src.scrutinycspm.resources.development.aws_s3bucket_scan import S3BucketRetriever
import json
import os

from tests.unit.base_test_case import BaseTestCase

class TestAWSEc2Scan(BaseTestCase):
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
        results = S3BucketRetriever(access_key, secret_key, region).run_scan()
        print(json.dumps(results, indent=4))
        self.assertIsNotNone(results)

