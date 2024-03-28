import unittest
from src.scrutinycspm.utils.encryption.certificate.json_encryption import JSONEncryption
from src.scrutinycspm.utils.encryption.certificate.certificate_utils import CertificateUtils
class TestJSONEncryption(unittest.TestCase):

    def setUp(self):
        self.private_cert_path = "path/to/cert"
        self.public_cert_path = "path/to/cert"

        # Generate a new certificate
        cert, private_key = CertificateUtils.generate_certificate(
            common_name="test",
            password="password"
        )

        self.encryption = JSONEncryption(private_key_path="", public_key_path="")

    def test_encrypt(self):
        # Test data
        data = {'key': 'value'}

        # Encrypt the data
        encrypted_data = self.encryption.encrypt(data)

        # Assert that the encrypted data is not empty
        self.assertIsNotNone(encrypted_data)

        # Add additional assertions if needed

    def test_decrypt(self):
        # Test data
        data = {'key': 'value'}
        password = 'password'

        # Encrypt the data
        encrypted_data = self.encryption.encrypt(data)

        # Decrypt the data
        decrypted_data = self.encryption.decrypt(encrypted_data, password)

        # Assert that the decrypted data matches the original data
        self.assertEqual(decrypted_data, data)

    def tearDown(self):
        # Clean up any resources used in the tests
        pass

if __name__ == '__main__':
    unittest.main()