import json
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

class JSONEncryption:
    def __init__(self, public_key_path: str, private_key_path: str):
        with open(public_key_path, "rb") as key_file:
            self.public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )
        self.private_key_path = private_key_path

    def encrypt(self, data: dict) -> bytes:
        json_data = json.dumps(data).encode('utf-8')
        encrypted_data = self.public_key.encrypt(
            json_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_data

    def decrypt(self, encrypted_data: bytes, password: str) -> dict:
        with open(self.private_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=password.encode('utf-8'),
                backend=default_backend()
            )
        decrypted_data = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        json_data = json.loads(decrypted_data.decode('utf-8'))
        return json_data