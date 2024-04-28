# Creating an AWS Credentials File with a Bash Script

This guide explains how to use a bash script to create an AWS credentials file (`.aws/credentials`) by prompting the user for the profile name, access key, and secret key.

## Prerequisites

- Bash shell environment
- AWS account and associated access key and secret key

## Script Content

Create a new file named `create_aws_credentials.sh` and add the following content:

```bash
#!/bin/bash

# Prompt for profile name
read -p "Enter the AWS profile name: " profile_name

# Prompt for access key
read -p "Enter the AWS access key: " access_key

# Prompt for secret key
read -s -p "Enter the AWS secret key: " secret_key
echo

# Create .aws directory if it doesn't exist
mkdir -p ~/.aws

# Write the credentials to the file
cat > ~/.aws/credentials <<EOF
[$profile_name]
aws_access_key_id = $access_key
aws_secret_access_key = $secret_key
EOF

echo "AWS credentials file created successfully!"
```
# Creating an AWS Credentials File with a Bash Script

This guide explains how to use a bash script to create an AWS credentials file (`.aws/credentials`) by prompting the user for the profile name, access key, and secret key.

## Prerequisites

- Bash shell environment
- AWS account and associated access key and secret key

## Script Content

Create a new file named `create_aws_credentials.sh` and add the following content:

```bash
#!/bin/bash

# Prompt for profile name
read -p "Enter the AWS profile name: " profile_name

# Prompt for access key
read -p "Enter the AWS access key: " access_key

# Prompt for secret key
read -s -p "Enter the AWS secret key: " secret_key
echo

# Create .aws directory if it doesn't exist
mkdir -p ~/.aws

# Write the credentials to the file
cat > ~/.aws/credentials <<EOF
[$profile_name]
aws_access_key_id = $access_key
aws_secret_access_key = $secret_key
EOF

echo "AWS credentials file created successfully!"

```
### Usage

Open a terminal or command prompt.

Navigate to the directory where you saved the create_aws_credentials.sh script.

Make the script executable by running the following command:

```bash
chmod +x create_aws_credentials.sh

```
Execute the script by running the following command:
```bash
./create_aws_credentials.sh
```
The script will prompt you to enter the following information:

AWS profile name: Enter a name for the profile as default
AWS access key: Enter your AWS access key.
AWS secret key: Enter your AWS secret key (the input will be hidden for security purposes).


After entering all the required information, the script will create the .aws/credentials file in your home directory.
The AWS credentials file will have the following format:

```bash
[default]
aws_access_key_id = access_key
aws_secret_access_key = secret_key
```
The script will display a success message indicating that the AWS credentials file has been created.

# Security Considerations - WARNING

Keep your AWS access key and secret key confidential and avoid sharing them or storing them in plain text.

Ensure that the create_aws_credentials.sh script file has appropriate access permissions to prevent unauthorized access.

Consider using more secure methods, such as AWS IAM roles or other access management solutions, for managing credentials in a production environment.