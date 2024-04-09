import unittest

from cryptography.hazmat.primitives.asymmetric import rsa

from src.scrutinycspm.utils.encryption.scanning_output_encryption.encrypt_output import OutputEncryptor


class TestOutputEncryptor(unittest.TestCase):
    def setUp(self):
        # Generate RSA key pair
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        self.public_key = self.private_key.public_key()

        # Initialize OutputEncryptor
        self.encryptor = OutputEncryptor()

    def test_encryption_decryption(self):
        # Test data
        data = {'message': 'Secret message'}

        # Encrypt data
        encrypted_key, encrypted_data, nonce = self.encryptor.encrypt(self.public_key, data)

        # Assert the encryption altered the data
        self.assertNotEquals(data, encrypted_data)

        # Decrypt data
        decrypted_data = self.encryptor.decrypt(self.private_key, encrypted_key, encrypted_data, nonce)

        # Assert original and decrypted data are equal
        self.assertEqual(data, decrypted_data)


if __name__ == '__main__':
    unittest.main()
