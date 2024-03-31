import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class CertificateUtils:
    @staticmethod
    def generate_certificate(
        # Warning: the days valid default parameter is set to 730 by default or 2 years, after that the certificate will expire!!!
        common_name: str, password: str, key_size: int = 2048, days_valid: int = 730
    ) -> tuple:
        # Generate a new private key
        private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=key_size, backend=default_backend()
        )

        # Create a self-signed certificate
        subject = issuer = x509.Name(
            [x509.NameAttribute(NameOID.COMMON_NAME, common_name)]
        )
        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(private_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.utcnow())
            .not_valid_after(
                datetime.datetime.utcnow() + datetime.timedelta(days=days_valid)
            )
            .add_extension(
                x509.SubjectAlternativeName([x509.DNSName(common_name)]),
                critical=False,
            )
            .sign(private_key, hashes.SHA256(), default_backend())
        )

        # Serialize the private key with password protection
        encrypted_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(
                password.encode("utf-8")
            ),
        )

        # Serialize the certificate
        cert_pem = cert.public_bytes(serialization.Encoding.PEM)

        return cert_pem, encrypted_private_key
    

    @staticmethod
    def generate_certificate_to_file(
        common_name: str, password: str, key_size: int = 2048, days_valid: int = 730
    ) -> tuple:
        cert_pem, encrypted_private_key = CertificateUtils.generate_certificate(
            common_name, password, key_size, days_valid
        )

        # Save the certificate to a file
        with open(f"{common_name}.crt", "wb") as f:
            f.write(cert_pem)

        # Save the private key to a file
        with open(f"{common_name}.key", "wb") as f:
            f.write(encrypted_private_key)

        # Extract the public key from the certificate
        cert = x509.load_pem_x509_certificate(cert_pem, default_backend())
        public_key = cert.public_key()

        # Serialize the public key
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Save the public key to a file
        with open(f"{common_name}.pub", "wb") as f:
            f.write(public_key_pem)

        return cert_pem, encrypted_private_key