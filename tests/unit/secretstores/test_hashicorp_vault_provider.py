from unittest import TestCase
from hydra.core.global_hydra import GlobalHydra
import hydra
from ScrutinyCSPM.src.scrutinycspm.access.securestores.hashicorp_vault_provider import HashicorpVaultProvider


class TestHashicorpVaultProvider(TestCase):

    def setUp(self):
        GlobalHydra.instance().clear()
        hydra.initialize(config_path="../../../conf", job_name="test_job", version_base="1.1")
        self.cfg = hydra.compose(config_name="vault")

        private_vault_config = self.cfg.vault.private_path

        GlobalHydra.instance().clear()
        hydra.initialize(config_path=private_vault_config, job_name="test_job_2", version_base="1.1")
        self.cfg_secure = hydra.compose(config_name="private_vault")

    def tearDown(self):
        GlobalHydra.instance().clear()

    def test_is_authenticate_wo_authentication(self):
        hc_provider = HashicorpVaultProvider(self.cfg_secure.vault.address, self.cfg_secure.vault.namespace)
        assert hc_provider.is_authenticated() == True

    def test_authenticate(self):
        hc_provider = HashicorpVaultProvider(self.cfg_secure.vault.address, self.cfg_secure.vault.namespace)
        hc_provider.authenticate_with_username_password(self.cfg_secure.vault.username,
                                                             self.cfg_secure.vault.password)
        assert hc_provider.is_authenticated() == True
