from typing import Protocol
from hvac import Client as HashicorpVaultClient
import hydra
from omegaconf import DictConfig
import sys

class HashicorpVaultPlugin(Protocol):
    def __init__(self, cfg: DictConfig, *args, **kwargs):
        self.client = HashicorpVaultClient(url=cfg.vault.address)

    def get_provider_name(self):
        return "hashicorp vault"

    def store_secret(self, name, value):
        # Writing a secret
        create_response = self.client.secrets.kv.v2.create_or_update_secret(
            path='name',
            secret=dict(password= value),
        )
        print('Secret written successfully.')

    def retrieve_secret(self, name):
        # Retrieving the secret
        read_response = self.client.secrets.kv.v2.read_secret_version(path='my-secret')
        password = read_response['data']['data']['password']
        print(f'Retrieved password: {password}')

    def list_providers(self):
        pass


    def authenticate(self, token, *args, **kwargs):
        # Authentication
        self.client.token = token
        return True