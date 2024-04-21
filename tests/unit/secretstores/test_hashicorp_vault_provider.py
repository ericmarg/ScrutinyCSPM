from unittest import TestCase
from hydra.core.global_hydra import GlobalHydra
import hydra
import os
from src.scrutinycspm.access.securestores.hashicorp_vault_provider import (
    HashicorpVaultProvider,
)
from tests.unit.base_test_case import BaseTestCase


class TestHashicorpVaultProvider(BaseTestCase):

    def setUp(self):
        super().setUp(config_path="../../conf", config_name="vault") 

    def test_is_authenticate_wo_authentication(self):
        hc_provider = HashicorpVaultProvider(
            self.cfg_secure.secrets.hc_vault.address,
            self.cfg_secure.secrets.hc_vault.namespace,
        )
        assert hc_provider.is_authenticated() == True

    def test_authenticate(self):
        hc_provider = HashicorpVaultProvider(
            self.cfg_secure.secrets.hc_vault.address,
            self.cfg_secure.secrets.hc_vault.namespace,
        )
        hc_provider.authenticate_with_username_password(
            username=self.cfg_secure.secrets.hc_vault.username,
            password=self.cfg_secure.secrets.hc_vault.password,
        )
        assert hc_provider.is_authenticated() == True

    def tearDown(self):
        GlobalHydra.instance().clear()
