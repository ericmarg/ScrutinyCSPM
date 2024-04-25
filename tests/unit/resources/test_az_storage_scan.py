import configparser
import os

from src.scrutinycspm.resources.development.azure.azure_storage_scan import AzureStorageAccount
from hydra.core.global_hydra import GlobalHydra
import json
import os

from tests.unit.base_test_case import BaseTestCase

class TestAzureStorageScanner(BaseTestCase):
    def setUp(self):
        super().setUp(config_path="../../conf", config_name="base-config") 

    def test_storage_scan(self):


        subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
        tenant_id = os.environ['AZURE_TENANT']
        client_id = os.environ['AZURE_CLIENT_ID']
        client_secret = os.environ['AZURE_SECRET']
        
        scanner = AzureStorageAccount(tenant_id=tenant_id, subscription_id=subscription_id, client_id=client_id, client_secret=client_secret, client_certificate=None)
        
        result = scanner.fetch_data()

        self.assertIsNotNone(result)

