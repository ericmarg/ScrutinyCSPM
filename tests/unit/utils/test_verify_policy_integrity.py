import os
import unittest

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

from src.scrutinycspm.utils.policy_verification.verify_policy_integrity import IntegrityChecker

digital_signature_path = 'dig_sig.bin'
message_path = 'message.bin'
public_key_path = 'public_key.pem'


class TestVerifyPolicyIntegrity(unittest.TestCase):
    def setUp(self):
        # Generate RSA keypair
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        self.public_key = self.private_key.public_key()

        # Save public key to file
        with open(public_key_path, 'wb') as f_public:
            f_public.write(self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

        # Digitally sign some sample data
        message = b"A message I want to sign"
        signature = self.private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        # Write the sample data to a file
        with open(message_path, 'wb') as f:
            f.write(message)

        # Write the digital signature to a file
        with open(digital_signature_path, 'wb') as f:
            f.write(signature)

    def test_verify_policy_integrity(self):
        # Test that verification passes when it should
        checker = IntegrityChecker(message_path, public_key_path)
        ret = checker.verify_policy(digital_signature_path)
        self.assertTrue(ret)

        # Modify message and check that verification returns false
        with open(message_path, 'ab') as f:
            f.write(b'foo')

        ret = checker.verify_policy(digital_signature_path)
        self.assertFalse(ret)

    def tearDown(self):
        os.remove(digital_signature_path)
        os.remove(public_key_path)
        os.remove(message_path)


if __name__ == '__main__':
    unittest.main()
