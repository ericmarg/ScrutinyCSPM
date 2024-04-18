import configparser
import os
import unittest
import hydra
from omegaconf import OmegaConf
from src.scrutinycspm.resources.development.s3bucket_scan import S3Scanner
from hydra.core.global_hydra import GlobalHydra
import json
import os

from tests.unit.base_test_case import BaseTestCase

class TestEc2Scan(BaseTestCase):
    def setUp(self):
        super().setUp(config_path="../../conf", config_name="vault") 

    def test_ec2_scan(self):
        
        

        credentials_path = self.cfg_secure.secrets.aws_credentials_file.path

        # Specify the path to the AWS credentials file
        aws_credentials_file = os.path.expanduser(credentials_path)