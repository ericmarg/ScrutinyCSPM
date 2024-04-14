import configparser
import os
import unittest
import hydra
from omegaconf import OmegaConf
from src.scrutinycspm.resources.development.s3bucket_scan import S3Scanner
from hydra.core.global_hydra import GlobalHydra
import json

class TestEc2Scan(unittest.TestCase):
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

    def test_ec2_scan(self):
        
        credentials_path = self.cfg_secure.secrets.aws_credentials_file.path

        # Specify the path to the AWS credentials file
        aws_credentials_file = os.path.expanduser(credentials_path)