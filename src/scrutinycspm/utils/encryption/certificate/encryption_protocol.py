from typing import Protocol

class EncryptionProtocol(Protocol):
    def encrypt(self, data: dict) -> bytes:
        ...

    def decrypt(self, encrypted_data: bytes, password: str) -> dict:
        ...