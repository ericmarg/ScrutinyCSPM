
import unittest
import hydra
import string
import random
from hydra.core.global_hydra import GlobalHydra

class BaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.default_config_path = "../../../conf"
        cls.default_config_name = "vault"

    def setUp(self, config_path=None, config_name=None):
        if config_path is None:
            config_path = self.default_config_path
        if config_name is None:
            config_name = self.default_config_name

        GlobalHydra.instance().clear()

        hydra.initialize(
            config_path=config_path,
            job_name=f"test_{self.generate_unique_name()}",
            version_base="1.1"
        )

        self.cfg = hydra.compose(config_name=config_name)

        private_vault_config = self.cfg.get("private_path")

        if private_vault_config:
            GlobalHydra.instance().clear()
            hydra.initialize(
                config_path=private_vault_config,
                job_name=f"test_{self.generate_unique_name()}_private",
                version_base="1.1"
            )
            self.cfg_secure = hydra.compose(config_name="private_vault")
        else:
            self.cfg_secure = self.cfg

    def generate_unique_name(self, length=8):
        characters = string.ascii_lowercase + string.digits
        unique_name = ''.join(random.choice(characters) for _ in range(length))
        return unique_name