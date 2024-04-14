import os
import sys
import boto3

# Prompt the user for AWS access key ID and secret access key
def configure_aws_credentials(profile_name):
    # Prompt the user for AWS access key ID and secret access key
    access_key_id = input("Enter your AWS access key ID: ")
    secret_access_key = input("Enter your AWS secret access key: ")
    
    # Configure the AWS credentials using boto3
    boto3.setup_default_session(aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    
    # Get the default credentials
    credentials = boto3.Session().get_credentials()
    
    # Get the path to the AWS credentials file
    aws_dir = os.path.expanduser("~/.aws")
    credentials_file = os.path.join(aws_dir, "credentials")
    
    # Create the ~/.aws directory if it doesn't exist
    os.makedirs(aws_dir, exist_ok=True)
    
    # Write the credentials to the file
    with open(credentials_file, "a") as f:
        f.write(f"[{profile_name}]\n")
        f.write(f"aws_access_key_id = {credentials.access_key}\n")
        f.write(f"aws_secret_access_key = {credentials.secret_key}\n")
        f.write("\n")  # Add a newline for separating profiles
    
    print(f"AWS credentials file configured successfully for profile '{profile_name}'!")
