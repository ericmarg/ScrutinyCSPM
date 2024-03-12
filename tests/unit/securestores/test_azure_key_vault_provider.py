from unittest import TestCase
from hydra.core.global_hydra import GlobalHydra
import hydra
from ScrutinyCSPM.src.scrutinycspm.access.securestores.azure_keyvault_provider import AzureKeyVaultProvider


class TestHashicorpVaultProvider(TestCase):

    def setUp(self):
        GlobalHydra.instance().clear()
        hydra.initialize(config_path="../../../conf", job_name="test_job", version_base="1.1")
        self.cfg = hydra.compose(config_name="vault")

        private_vault_config = self.cfg.vault.private_path

        GlobalHydra.instance().clear()
        hydra.initialize(config_path=private_vault_config, job_name="test_job_2", version_base="1.1")
        self.cfg_secure = hydra.compose(config_name="private_vault")

    def test_certificate_authentication(self):
        akv_provider = AzureKeyVaultProvider(self.cfg_secure.vault.key_vault_url)
        assert akv_provider.authenticate_with_certificate(self.cfg_secure.vault.tenant_id, self.cfg_secure.vault.client_id, certificate_path=self.cfg_secure.vault.certificate_path)


    def test_read_secret(self):
        akv_provider = AzureKeyVaultProvider(self.cfg_secure.vault.key_vault_url)
        akv_provider.authenticate_with_certificate(self.cfg_secure.vault.tenant_id, self.cfg_secure.vault.client_id, certificate_path=self.cfg_secure.vault.certificate_path)
        print(akv_provider.read_secret("hashicorp-vault-password02"))
        assert akv_provider.read_secret("hashicorp-vault-password02") == {'value': 'password12345'}

    def tearDown(self):
        GlobalHydra.instance().clear()