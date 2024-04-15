import json
import os
from typing import Dict

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class OutputEncryptor():
    def __init__(self, block_size=128):
        self.block_size = block_size
        self.block_bytes = self.block_size // 8

    def encrypt(self, public_key, data: Dict):
        byte_data = json.dumps(data).encode('utf-8')

        # Generate random numbers for encryption
        key = os.urandom(self.block_bytes)
        nonce = os.urandom(self.block_bytes)

        # Using a reversible encryption cipher, encrypt the text data using the symmetric key
        cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
        encryptor = cipher.encryptor()
        cipher_text = encryptor.update(byte_data) + encryptor.finalize()

        # Encrypt the symmetric key using the public key extracted from the certificate via asymmetric encryption
        encrypted_key = public_key.encrypt(
            key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        # Append the encrypted symmetric key and text data together and send them to the recipient
        return encrypted_key, cipher_text, nonce

    def decrypt(self, private_key, encrypted_key, cipher_text, nonce):
        decrypted_key = private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Instantiate the cipher object using the decrypted key and nonce
        cipher = Cipher(algorithms.AES(decrypted_key), modes.CTR(nonce))
        decryptor = cipher.decryptor()

        # Decrypt the message
        decrypted_bytes = decryptor.update(cipher_text) + decryptor.finalize()

        # Return it as a JSON object
        return json.loads(decrypted_bytes.decode('utf-8'))
