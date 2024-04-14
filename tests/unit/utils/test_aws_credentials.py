import os
import unittest
import hydra
from omegaconf import OmegaConf
from hydra.core.global_hydra import GlobalHydra
from src.scrutinycspm.utils.aws_credential_file import configure_aws_credentials

class TestAWSCredentialsUtils(unittest.TestCase):
    def setUp(self):

        GlobalHydra.instance().clear()
        hydra.initialize(
            config_path="../../../conf", job_name="test_s3scan", version_base="1.1"
        )
        self.cfg = hydra.compose(config_name="vault")

        private_vault_config = self.cfg.private_path

        GlobalHydra.instance().clear()
        hydra.initialize(
            config_path=private_vault_config, job_name="test_s3scan_private", version_base="1.1"
        )
        self.cfg_secure = hydra.compose(config_name="private_vault")

    def test_generate_aws_credential_file(self):

        credentials_path = self.cfg_secure.secrets.aws_credentials_file.path
        configure_aws_credentials("default")
        
        # Assert that the generated AWS credentials file exists
        self.assertTrue(os.path.exists(credentials_path))