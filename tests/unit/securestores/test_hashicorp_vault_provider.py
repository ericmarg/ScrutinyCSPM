from unittest import TestCase
from hydra.core.global_hydra import GlobalHydra
import hydra
from ScrutinyCSPM.src.scrutinycspm.access.securestores.hashicorp_vault_provider import HashicorpVaultProvider

class TestHashicorpVaultProvider(TestCase):
    def test_authenticate(self):
        GlobalHydra.instance().clear()
        hydra.initialize(config_path="../../../conf", job_name="test_job", version_base="1.1")
        cfg = hydra.compose(config_name="vault")
        # the private_vaults yaml file is not included in the repository
        # however, we want the test connection to Hashicorp Vault
        private_vault_config = cfg.vault.private_path

        GlobalHydra.instance().clear()
        hydra.initialize(config_path=private_vault_config, job_name="test_job_2", version_base="1.1")
        cfg_secure = hydra.compose(config_name="private_vault")
        print(cfg_secure.vault.address)

        hc_provider = HashicorpVaultProvider(cfg_secure.vault.address, cfg_secure.vault.namespace)
        hc_provider.authenticate_with_username_password(cfg_secure.vault.username, cfg_secure.vault.password)
        assert True
        # assert False