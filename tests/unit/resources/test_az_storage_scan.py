import configparser
import os

from src.scrutinycspm.resources.development.azure.azure_storage_scan import AzureStorageScanner
from hydra.core.global_hydra import GlobalHydra
import json
import os

from tests.unit.base_test_case import BaseTestCase

class TestAzureStorageScanner(BaseTestCase):
    def setUp(self):
        super().setUp(config_path="../../conf", config_name="vault") 

    def test_storage_scan(self):

        credentials_path = self.cfg_secure.secrets.aws_credentials_file.path

        # Specify the path to the AWS credentials file
        aws_credentials_file = os.path.expanduser(credentials_path)
        config = configparser.ConfigParser()
        config.read(aws_credentials_file)
        subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
        tenant_id = os.environ['AZURE_TENANT']
        client_id = os.environ['AZURE_CLIENT_ID']
        client_secret = os.environ['AZURE_SECRET']
        
        results = AzureStorageScanner(subscription_id=subscription_id, tenant_id=tenant_id, client_id=client_id, client_secret=client_secret).run_scan()
        print(json.dumps(results, indent=4))
        self.assertIsNotNone(results)

