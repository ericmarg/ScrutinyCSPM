import os
import configparser
from hydra.core.global_hydra import GlobalHydra
from src.scrutinycspm.utils.aws_credential_file import configure_aws_credentials
from tests.unit.base_test_case import BaseTestCase

class TestAWSCredentialsUtils(BaseTestCase):
    def setUp(self):

        super().setUp(config_path="../../conf", config_name="base-config")

    def test_generate_aws_credential_file(self):

        credentials_path = self.cfg_secure.secrets.aws_credentials_file.path
        configure_aws_credentials("default", )
        
        # Assert that the generated AWS credentials file exists
        self.assertTrue(os.path.exists(credentials_path))

    def test_generate_aws_credential_file_with_profile(self):
            
        credentials_path = self.cfg_secure.secrets.aws_credentials_file.path
        configure_aws_credentials("default", profile="test_profile")
        
        # Assert that the generated AWS credentials file exists
        self.assertTrue(os.path.exists(credentials_path))
   