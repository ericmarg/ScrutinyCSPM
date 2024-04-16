import subprocess
import unittest

from src.scrutinycspm.utils.encryption.ansible.ansible_vault_encryption import decrypt_yaml, encrypt_yaml


class TestYamlCrypto(unittest.TestCase):
    def setUp(self):
        self.password = "secret_password"
        self.input_file = "input.yaml"
        self.encrypted_file = "encrypted.yaml"
        self.decrypted_file = "decrypted.yaml"

        with open(self.input_file, 'w') as file:
            file.write("key: value")

    def test_encrypt_decrypt(self):
        encrypt_yaml(self.input_file, self.encrypted_file, self.password)
        decrypt_yaml(self.encrypted_file, self.decrypted_file, self.password)

        with open(self.decrypted_file, 'r') as file:
            decrypted_content = file.read()

        self.assertEqual(decrypted_content, "key: value")

    def tearDown(self):
        subprocess.run(f"rm {self.input_file} {self.encrypted_file} {self.decrypted_file}", shell=True)
