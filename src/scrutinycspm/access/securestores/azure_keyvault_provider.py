from azure.core.exceptions import ClientAuthenticationError
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential, CredentialUnavailableError
from azure.identity import CertificateCredential
import logging
from typing import Dict, Any
from omegaconf import DictConfig, OmegaConf


class AzureKeyVaultProvider:
    def __init__(self, vault_url: str, log_config: DictConfig = OmegaConf.create({"logging": {"level": {"azure_key_vault_provider": "INFO"}}})):
        self.vault_url = vault_url
        self.client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())

        logger = logging.getLogger(__name__)
    def authenticate_with_certificate(tenant_id: str, client_id: str, certificate_path: str):

        try:
            credential = CertificateCredential(
                tenant_id=tenant_id,
                client_id=client_id,
                certificate_path=certificate_path
            )
            return credential
        except CredentialUnavailableError as no_cert:

            return None
        except ClientAuthenticationError as credential_error:
            return None



    def is_authenticated(self) -> bool:
        try:
            # Perform a simple operation to check authentication
            self.client.list_properties_of_secrets()
            return True
        except Exception:
            return False

    def read_secret(self, secret_name: str, version: str = None, **kwargs: Any) -> Dict[str, Any]:
        try:
            if version is None:
                secret = self.client.get_secret(secret_name, **kwargs)
            else:
                secret = self.client.get_secret(secret_name, version=version, **kwargs)

            return {"value": secret.value}

        except Exception as e:
            raise Exception(f"An error occurred while reading secret '{secret_name}': {str(e)}") from e

    def write_secret(self, secret_name: str, secret_value: str, **kwargs: Any) -> None:
        try:
            self.client.set_secret(secret_name, secret_value, **kwargs)
        except Exception as e:
            raise Exception(f"An error occurred while writing secret '{secret_name}': {str(e)}") from e