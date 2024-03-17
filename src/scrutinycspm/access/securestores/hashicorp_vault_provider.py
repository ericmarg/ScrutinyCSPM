import hvac
from typing import Dict, Any
import hvac.exceptions

class HashicorpVaultProvider:

    def __init__(self, vault_url: str, namespace: str) -> None:
        """
        Initializes the HashicorpVaultProvider with the given vault_url and namespace.

        Parameters
        ----------
        vault_url : str
            The URL of the Hashicorp Vault.
        namespace : str
            The namespace to use for the Hashicorp Vault.
        """
        self.client = hvac.Client(url=vault_url, namespace=namespace)

    def authenticate_with_username_password(self, username: str, password: str) -> None:
        """
        Authenticates the client with the given username and password.

        Parameters
        ----------
        username : str
            The username to use for authentication.
        password : str
            The password to use for authentication.

        Raises
        ------
        Exception
            If the authentication fails.
        """
        try:
            auth_response = self.client.auth.userpass.login(username=username, password=password)
            self.client.token = auth_response["auth"]["client_token"]
        except hvac.exceptions.InvalidRequest as e:
            raise ValueError("Invalid username or password") from e
        except hvac.exceptions.Forbidden as e:
            raise PermissionError("Insufficient permissions to authenticate") from e
        except hvac.exceptions.VaultError as e:
            raise Exception("Vault error occurred while authenticating") from e
        except Exception as e:
            raise Exception("An error occurred while authenticating") from e


    def read_secret(self, path: str, mount_point: str = "secret", version: int = None, **kwargs: Any) -> Dict[
        str, Any]:
        try:
            if version is None:
                response = self.client.secrets.kv.v2.read_secret_version(path=path, mount_point=mount_point,
                                                                         **kwargs)
            else:
                response = self.client.secrets.kv.v2.read_secret_version(path=path, mount_point=mount_point,
                                                                         version=version, **kwargs)

            if response:
                return response["data"]["data"]
            else:
                raise ValueError(f"Secret not found at path: {path}")

        except hvac.exceptions.InvalidPath as e:
            raise ValueError(f"Invalid path: {path}") from e
        except hvac.exceptions.Forbidden as e:
            raise PermissionError(f"Insufficient permissions to read secret at path: {path}") from e
        except hvac.exceptions.VaultError as e:
            raise Exception(f"Vault error occurred while reading secret at path: {path}") from e
        except Exception as e:
            raise Exception(f"An error occurred while reading secret at path: {path}") from e

    def is_authenticated(self) -> bool:
        try:
            # Perform a simple operation to check authentication
            if self.client.token is None:
                return False
            else:
                self.client.sys.read_health_status()
                return True
        except hvac.exceptions.Forbidden:
            return False
        except hvac.exceptions.VaultError:
            return False
