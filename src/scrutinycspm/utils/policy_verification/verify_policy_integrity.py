from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key


# Verifies that the policy at the provided path has not been altered using the digital signature of the policy writer.
# The policy writer must sign using the SHA256 hashing algorithm. The digital signature loaded from a file, so a sig-
# nature file should be provided with the corresponding policy. The writer must also make their public key available.
class IntegrityChecker:
    def __init__(self, policy_path: str, public_key_path: str, hash_algorithm='SHA256'):
        self.policy_path = policy_path
        self.public_key_path = public_key_path
        self.hash_algorithm = hash_algorithm
        self.public_key = self._load_public_key()

    # Loads the public key of the policy writer from a provided file path
    def _load_public_key(self):
        try:
            with open(self.public_key_path, 'rb') as f:
                public_key = load_pem_public_key(f.read())
            return public_key
        except (ValueError, UnsupportedAlgorithm) as e:
            print(f"Error loading public key: {e}")
            return None

    # Uses the cryptography library's public/private key verification to check a file has not been altered.
    # Takes the file path to the digital signature as input.
    # Returns True if the file could be verified or False if the file has been altered.
    def verify_policy(self, digital_signature_path: str) -> bool:
        if not self.public_key:
            print("Public key not loaded.")
            return False

        # Read policy file
        try:
            with open(self.policy_path, 'rb') as f:
                policy = f.read()
        except FileNotFoundError:
            print(f"Policy file '{self.policy_path}' not found")
            return False

        # Read and verify the digital signature
        try:
            with open(digital_signature_path, 'rb') as f:
                signature = f.read()
                self.public_key.verify(
                    signature,
                    policy,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
        except (FileNotFoundError, InvalidSignature) as e:
            print(f"Verification failed: {e}")
            return False

        return True
