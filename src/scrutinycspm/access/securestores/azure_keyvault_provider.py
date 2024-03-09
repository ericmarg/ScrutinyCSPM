from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from typing import Dict, Any

class AzureKeyVaultProvider:
    def __init__(self, vault_url: str):
        self.vault_url = vault_url
        self.client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())

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