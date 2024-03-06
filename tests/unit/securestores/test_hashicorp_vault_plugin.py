from unittest import TestCase
from omegaconf import OmegaConf
from hydra.core.global_hydra import GlobalHydra
from omegaconf import DictConfig
import hydra

from ScrutinyCSPM.src.scrutinycspm.access.securestores.hashicorp_vault_plugin import HashicorpVaultPlugin


class TestAwsSecureStorePlugin(TestCase):
    def test_authenticate(self):
        GlobalHydra.instance().clear()
        hydra.initialize(config_path="../../../conf", job_name="test_job")
        cfg = hydra.compose(config_name="vault")
        # the private_vaults yaml file is not included in the repository
        # however, we want the test connection to Hashicorp Vault
        private_vault_config = cfg.vault.private_path

        GlobalHydra.instance().clear()
        hydra.initialize(config_path=private_vault_config, job_name="test_job_2")
        cfg_secure = hydra.compose(config_name="private_vault")

        hv = HashicorpVaultPlugin(cfg_secure)
        self.assertTrue(hv.authenticate("my_token"))

        GlobalHydra.instance().clear()

