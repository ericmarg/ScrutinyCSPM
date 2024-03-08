import hvac
from typing import Dict, Any

class HashicorpVaultSecretRetriever:
    def __init__(self, vault_url: str):
        self.client = hvac.Client(url=vault_url)

    def authenticate_with_username_password(self, username: str, password: str) -> None:
        auth_response = self.client.auth.userpass.login(username=username, password=password)
        if auth_response.status_code == 200:
            self.client.token = auth_response.json()["auth"]["client_token"]
        else:
            raise Exception("Authentication failed.")

    def authenticate_with_token(self, token: str) -> None:
        self.client.token = token

    def read_secret(self, secret_path: str) -> Dict[str, Any]:
        read_response = self.client.secrets.kv.v2.read_secret_version(path=secret_path)
        return read_response["data"]["data"]

    def write_secret(self, secret_path: str, secret_data: Dict[str, Any]) -> None:
        self.client.secrets.kv.v2.create_or_update_secret(path=secret_path, secret=secret_data)