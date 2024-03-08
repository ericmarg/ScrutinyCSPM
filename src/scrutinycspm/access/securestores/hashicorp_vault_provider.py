import hvac
from typing import Dict, Any

class HashicorpVaultProvider:
    """
    A class used to interact with Hashicorp Vault.

    ...

    Attributes
    ----------
    client : hvac.Client
        a client instance to interact with the Hashicorp Vault

    Methods
    -------
    __init__(self, vault_url: str, namespace: str) -> None:
        Initializes the HashicorpVaultProvider with the given vault_url and namespace.

    authenticate_with_username_password(self, username: str, password: str) -> None:
        Authenticates the client with the given username and password.

    authenticate_with_token(self, token: str) -> None:
        Authenticates the client with the given token.

    read_secret(self, secret_path: str) -> Dict[str, Any]:
        Reads the secret at the given secret_path.

    write_secret(self, secret_path: str, secret_data: Dict[str, Any]) -> None:
        Writes the given secret_data at the given secret_path.
    """

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
        auth_response = self.client.auth.userpass.login(username=username, password=password)
        if self.client.is_authenticated():
            print("authenticated successfully.")
            self.client.token = auth_response["auth"]["client_token"]
        else:
            raise Exception("Authentication failed.")