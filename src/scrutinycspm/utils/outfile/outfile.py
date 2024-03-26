from abc import ABC, abstractmethod
from typing import Dict

from src.scrutinycspm.utils.encryption.certificate.json_encryption import JSONEncryption


class OutputFileCreator(ABC):
    @abstractmethod
    def create_output_file(self, json_data: Dict, public_key_path: str, private_key_path: str, file_name: str) -> str:
        pass


# Implements the create_output_file(Dict) method. This method takes JSON data and public and private key path strings
# as input, and encrypts it, then saves it to a file and returns the file name string.
class JSONOutputFileCreator(OutputFileCreator):
    def create_output_file(self, json_data: Dict, public_key_path: str, private_key_path: str,
                           file_name='scrutiny_outfile.bin') -> str:
        # Create an instance of JSONEncryption
        json_encryption = JSONEncryption(public_key_path, private_key_path)

        # Encrypt the JSON into byte data
        encrypted_data = json_encryption.encrypt(json_data)

        try:
            # Save the encrypted data to a binary file
            with open(file_name, 'wb') as outfile:
                outfile.write(encrypted_data)
        except OSError as err:
            # Re-raise the exception with a custom error message
            raise OSError(f"Failed to write to file '{file_name}': {err}") from err

        # Return the file name
        return file_name
