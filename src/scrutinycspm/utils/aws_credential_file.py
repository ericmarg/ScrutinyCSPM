import os
import configparser
import boto3

# Prompt the user for AWS access key ID and secret access key
def configure_aws_credentials(profile_name, access_key_id, secret_access_key, aws_configurations_path = "~/.aws"):
  
    # Configure the AWS credentials using boto3
    boto3.setup_default_session(aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    
    # Get the path to the AWS credentials file
    aws_dir = os.path.expanduser(aws_configurations_path)
    credentials_file = os.path.join(aws_dir, "credentials")
    
    # Create the ~/.aws directory if it doesn't exist
    os.makedirs(aws_dir, exist_ok=True)
    
    # Write the credentials to the file
    with open(credentials_file, "a") as f:
        f.write(f"[{profile_name}]\n")
        f.write(f"aws_access_key_id = {access_key_id}\n")
        f.write(f"aws_secret_access_key = {secret_access_key}\n")
        f.write("\n")  # Add a newline for separating profiles
    
    print(f"AWS credentials file configured successfully for profile '{profile_name}'!")

def remove_profile(profile_name, aws_configurations_path = "~/.aws/credentials"):

    # Get the path to the AWS configuration file
    aws_config_path = os.path.expanduser(aws_configurations_path)

    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the configuration file
    config.read(aws_config_path)

    # Check if the specified profile exists
    if profile_name in config.sections():
        # Remove the profile
        config.remove_section(profile_name)

        # Write the updated configuration back to the file
        with open(aws_config_path, "w") as config_file:
            config.write(config_file)

        print(f"Profile '{profile_name}' has been removed from the AWS configuration file.")
    else:
        print(f"Profile '{profile_name}' does not exist in the AWS configuration file.")

def main():
    profile_name = input("Enter the profile name: ")
    
    access_key_id = input("Enter your AWS access key ID: ")
    secret_access_key = input("Enter your AWS secret access key: ")

    configure_aws_credentials(profile_name, access_key_id, secret_access_key)

    remove_profile(profile_name="testing04")

if __name__ == "__main__":
    main()