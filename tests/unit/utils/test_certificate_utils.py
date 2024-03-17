import unittest
import src.scrutinycspm.utils.encryption.certificate.certificate_utils as utils

class TestCertificateUtils(unittest.TestCase):

    def test_generate_certificate(self):
        common_name = "example.com"
        password = "password"
        key_size = 2048
        days_valid = 730

        cert_pem, encrypted_private_key = utils.CertificateUtils.generate_certificate(common_name, password, key_size, days_valid)

        # Assert that the generated certificate PEM is not empty
        self.assertTrue(cert_pem)

        # Assert that the generated encrypted private key is not empty
        self.assertTrue(encrypted_private_key)

        # TODO: Add more specific assertions to validate the generated certificate and private key
