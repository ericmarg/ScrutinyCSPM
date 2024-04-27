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