from unittest import TestCase
from hydra.core.global_hydra import GlobalHydra
import hydra
from src.scrutinycspm.access.securestores.azure_keyvault_provider import (
    AzureKeyVaultProvider,
)

from datetime import datetime
from tests.unit.base_test_case import BaseTestCase


class TestAzureKeyVaultProvider(BaseTestCase):
    """
    This class contains unit tests for the AzureKeyVaultProvider class.
    """

    def setUp(self):
        super().setUp(config_path="../../conf", config_name="base-config") 

    def test_certificate_authentication(self):
        akv_provider = AzureKeyVaultProvider(
            self.cfg_secure.secrets.azure_key_vault.url
        )
        assert akv_provider.authenticate_with_certificate(
            self.cfg_secure.secrets.azure_key_vault.tenant_id,
            self.cfg_secure.secrets.azure_key_vault.client_id,
            certificate_path=self.cfg_secure.secrets.azure_key_vault.certificate_path,
        )

    def test_read_secret(self):
        akv_provider = AzureKeyVaultProvider(
            self.cfg_secure.secrets.azure_key_vault.url
        )
        akv_provider.authenticate_with_certificate(
            self.cfg_secure.secrets.azure_key_vault.tenant_id,
            self.cfg_secure.secrets.azure_key_vault.client_id,
            certificate_path=self.cfg_secure.secrets.azure_key_vault.certificate_path,
        )
        print(akv_provider.read_secret("hashicorp-vault-password02"))
        assert akv_provider.read_secret("hashicorp-vault-password02") == {
            "value": "password12345"
        }

    def test_write_secret(self):
        akv_provider = AzureKeyVaultProvider(
            self.cfg_secure.secrets.azure_key_vault.url
        )
        akv_provider.authenticate_with_certificate(
            self.cfg_secure.secrets.azure_key_vault.tenant_id,
            self.cfg_secure.secrets.azure_key_vault.client_id,
            certificate_path=self.cfg_secure.secrets.azure_key_vault.certificate_path,
        )
        # Get the current date
        current_date = datetime.now()

        # Format the date as a string
        date_string = current_date.strftime("%Y-%m-%d")
        print(akv_provider.read_secret("updates-test01"))
        akv_provider.write_secret("updates-test01", date_string)
        assert akv_provider.read_secret("updates-test01") == {"value": f"{date_string}"}

    def tearDown(self):
        GlobalHydra.instance().clear()
