from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.identity import CertificateCredential

import logging
from typing import Dict, Any
from omegaconf import DictConfig, OmegaConf


class AzureKeyVaultProvider:
    def __init__(self, vault_url: str, log_config: DictConfig = OmegaConf.create(
        {"logging": {"level": {"azure_key_vault_provider": "ERROR"}}})):
        self.vault_url = vault_url
        self.logger = logging.getLogger(__name__)

    def authenticate_with_certificate(self, tenant_id: str, client_id: str, certificate_path: str):
        try:

            credential = CertificateCredential(
                tenant_id=tenant_id,
                client_id=client_id,
                certificate_path=certificate_path
            )

            # Use the credential with SecretClient
            self.secret_client = SecretClient(vault_url=self.vault_url, credential=credential)
            return True
        except Exception as e:
            self.logger.error(f"An error occurred while authenticating with certificate: {str(e)}")
            raise Exception(f"An error occurred while authenticating with certificate: {str(e)}") from e

    def is_authenticated(self, credential) -> bool:
        try:
            # Perform a simple operation to check authentication
            if self.secret_client is not None:
                return True
        except Exception:
            return False

    def read_secret(self, secret_name: str, version: str = None, **kwargs: Any) -> Dict[str, Any]:
        try:
            if version is None:
                secret = self.secret_client.get_secret(secret_name, **kwargs)
            else:
                secret = self.secret_client.get_secret(secret_name, version=version, **kwargs)

            return {"value": secret.value}

        except Exception as e:
            raise Exception(f"An error occurred while reading secret '{secret_name}': {str(e)}") from e

    def write_secret(self, secret_name: str, secret_value: str, **kwargs: Any) -> None:
        try:
            self.secret_client.set_secret(secret_name, secret_value, **kwargs)
        except Exception as e:
            self.logger.error(f"An error occurred while writing secret{secret_name}': {str(e)}")
            raise Exception(f"An error occurred while writing secret '{secret_name}': {str(e)}") from e
