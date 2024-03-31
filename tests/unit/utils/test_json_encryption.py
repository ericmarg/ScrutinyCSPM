import unittest
from src.scrutinycspm.utils.encryption.certificate.json_encryption import JSONEncryption
from src.scrutinycspm.utils.encryption.certificate.certificate_utils import (
    CertificateUtils,
)
import os


class TestJSONEncryption(unittest.TestCase):

    def setUp(self):
        self.common_name = "common-name-test"
        self.private_cert_path = f"{self.common_name}.key"
        self.public_cert_path = f"{self.common_name}.pub"
        self.password = "password"
        self.path_to_encrypted_file = "secret-stuff.txt"

        CertificateUtils.generate_certificate_to_file(self.common_name, self.password)

    def test_cedrtificate_files_exist(self):
        # Assert that the private key file exists
        self.assertTrue(os.path.exists(self.private_cert_path))

        # Assert that the public key file exists
        self.assertTrue(os.path.exists(self.public_cert_path))

    def test_encrypt(self):

        self.encryption = JSONEncryption(
            private_key_path=self.private_cert_path,
            public_key_path=self.public_cert_path,
        )

        # Test data
        data = {"key": "value"}

        # Encrypt the data
        encrypted_data = self.encryption.encrypt(data)

        # Assert that the encrypted data is not empty
        self.assertIsNotNone(encrypted_data)

        # Add additional assertions if needed

    def test_decrypt(self):

        self.encryption = JSONEncryption(
            public_key_path=self.public_cert_path,
            private_key_path=self.private_cert_path,
        )

        # Test data
        data = {"key": "value"}

        # Encrypt the data
        encrypted_data = self.encryption.encrypt(data)
        # Assert that the encrypted data is not empty
        self.assertIsNotNone(encrypted_data)

        with open(self.path_to_encrypted_file, "wb") as file:
            file.write(encrypted_data)

        # Decrypt the data
        decrypted_data = self.encryption.decrypt_from_file(
            self.path_to_encrypted_file, self.password
        )

        # Decrypt the data
        decrypted_data = self.encryption.decrypt(encrypted_data, self.password)

        # Assert that the decrypted data matches the original data
        self.assertEqual(decrypted_data, data)

    def tearDown(self):
        # Clean up any resources used in the tests
        if os.path.exists(self.path_to_encrypted_file):
            os.remove(self.path_to_encrypted_file)

        if os.path.exists(self.private_cert_path):
            os.remove(self.private_cert_path)

        if os.path.exists(self.public_cert_path):
            os.remove(self.public_cert_path)


if __name__ == "__main__":
    unittest.main()
