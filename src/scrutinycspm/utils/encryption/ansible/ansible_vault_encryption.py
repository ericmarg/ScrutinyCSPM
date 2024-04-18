import subprocess
import tempfile

def encrypt_yaml(file_path, output_file, password):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write(password)
        temp_file.flush()
        command = f"ansible-vault encrypt --vault-password-file={temp_file.name} --output={output_file} {file_path}"
        subprocess.run(command, shell=True, check=True)
    print(f"YAML file encrypted and saved as {output_file}")

def decrypt_yaml(file_path, output_file, password):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write(password)
        temp_file.flush()
        command = f"ansible-vault decrypt --vault-password-file={temp_file.name} --output={output_file} {file_path}"
        subprocess.run(command, shell=True, check=True)
    print(f"YAML file decrypted and saved as {output_file}")