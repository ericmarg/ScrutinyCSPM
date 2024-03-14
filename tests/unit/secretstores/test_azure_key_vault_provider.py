from unittest import TestCase
from hydra.core.global_hydra import GlobalHydra
import hydra
from src.scrutinycspm.access.securestores.azure_keyvault_provider import AzureKeyVaultProvider

from datetime import datetime

class TestAzureKeyVaultProvider(TestCase):

    def setUp(self):
        GlobalHydra.instance().clear()
        hydra.initialize(config_path="../../../conf", job_name="test_job", version_base="1.1")
        self.cfg = hydra.compose(config_name="vault")

        private_vault_config = self.cfg.private_path

        GlobalHydra.instance().clear()
        hydra.initialize(config_path=private_vault_config, job_name="test_job_2", version_base="1.1")
        self.cfg_secure = hydra.compose(config_name="private_vault")

    def test_certificate_authentication(self):
        akv_provider = AzureKeyVaultProvider(self.cfg_secure.secrets.azure_key_vault.url)
        assert akv_provider.authenticate_with_certificate(self.cfg_secure.secrets.azure_key_vault.tenant_id, self.cfg_secure.secrets.azure_key_vault.client_id, certificate_path=self.cfg_secure.secrets.azure_key_vault.certificate_path)


    def test_read_secret(self):
        akv_provider = AzureKeyVaultProvider(self.cfg_secure.secrets.azure_key_vault.url)
        akv_provider.authenticate_with_certificate(self.cfg_secure.secrets.azure_key_vault.tenant_id, self.cfg_secure.secrets.azure_key_vault.client_id, certificate_path=self.cfg_secure.secrets.azure_key_vault.certificate_path)
        print(akv_provider.read_secret("hashicorp-vault-password02"))
        assert akv_provider.read_secret("hashicorp-vault-password02") == {'value': 'password12345'}

    def test_write_secret(self):
        akv_provider = AzureKeyVaultProvider(self.cfg_secure.secrets.azure_key_vault.url)
        akv_provider.authenticate_with_certificate(self.cfg_secure.secrets.azure_key_vault.tenant_id, self.cfg_secure.secrets.azure_key_vault.client_id, certificate_path=self.cfg_secure.secrets.azure_key_vault.certificate_path)
        # Get the current date
        current_date = datetime.now()

        # Format the date as a string
        date_string = current_date.strftime("%Y-%m-%d")
        print(akv_provider.read_secret("updates-test01"))
        akv_provider.write_secret("updates-test01", date_string)
        assert akv_provider.read_secret("updates-test01") == {'value': f'{date_string}'}
    
    def tearDown(self):
        GlobalHydra.instance().clear()