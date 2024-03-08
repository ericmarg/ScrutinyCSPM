from typing import Protocol, Dict, Any

class SecretRetriever(Protocol):
    def authenticate_with_username_password(self, username: str, password: str) -> None:
        ...

    def authenticate_with_token(self, token: str) -> None:
        ...

    def read_secret(self, secret_path: str) -> Dict[str, Any]:
        ...

    def write_secret(self, secret_path: str, secret_data: Dict[str, Any]) -> None:
        ...