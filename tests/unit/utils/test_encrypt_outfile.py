import json
import os
import unittest

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

from src.scrutinycspm.utils.encryption.outfile.encrypt_outfile import *

OUTFILE_PATH = 'scrutiny_outfile.bin'

PRIVATE_KEY_PATH = 'private_key.pem'

PUBLIC_KEY_PATH = 'public_key.pem'


# Modified Rob's decryption function to remove the password requirement for testing
def decrypt(encrypted_data: bytes) -> dict:
    with open(PRIVATE_KEY_PATH, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
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


class TestJSONOutputFileCreator(unittest.TestCase):
    def setUp(self):
        # Generate RSA key pair
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        self.public_key = self.private_key.public_key()
        self.sample_data = {'message': 'JSON data to be encrypted and saved to file'}

        # Save public and private keys to files
        with open(PUBLIC_KEY_PATH, 'wb') as f_public:
            f_public.write(self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

        with open(PRIVATE_KEY_PATH, 'wb') as f_private:
            f_private.write(self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

    def test_create_output_file(self):
        creator = JSONOutputFileCreator()
        output_file = creator.create_output_file(self.sample_data, PUBLIC_KEY_PATH, PRIVATE_KEY_PATH)

        # Assert that output_file is not None
        self.assertIsNotNone(output_file)

    def test_decrypt(self):
        # Ensure that test_create_output_file has been executed
        self.test_create_output_file()

        with open(OUTFILE_PATH, 'rb') as file:
            file_content = file.read()

        # Instantiate encryption helper class
        json_encryption = JSONEncryption(PUBLIC_KEY_PATH, PRIVATE_KEY_PATH)

        # Decrypt the file
        decrypted_data = decrypt(file_content)

        self.assertEqual(decrypted_data, self.sample_data)

    def tearDown(self):
        os.remove(PUBLIC_KEY_PATH)
        os.remove(PRIVATE_KEY_PATH)
        os.remove(OUTFILE_PATH)


if __name__ == '__main__':
    unittest.main()
