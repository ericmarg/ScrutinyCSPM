# Setting Azure Environment Variables with set_azure_env_vars.sh

This document explains how to use the `set_azure_env_vars.sh` bash script to set Azure environment variables and update the `.bashrc` file.

## Prerequisites

- Bash shell environment
- Azure subscription and associated credentials

## Script Content

To use the current version of Scrutiny CSPM, you will need to create environment variables, either locally or in your container. 

At the root of this project `set_azure_env_vars.sh` the following content:

```bash
#!/bin/bash

echo "This script will set the following environment variables: AZURE_SUBSCRIPTION_ID, AZURE_TENANT, AZURE_CLIENT_ID, AZURE_SECRET"
echo "SECURITY WARNING: This script will append the environment variables to the end of the .bashrc file in the home directory."
echo "Use this script only if you are sure you want to set these environment variables."
echo "Do you want to continue? (y/n)"
read CONTINUE


echo "Enter the value for AZURE_SUBSCRIPTION_ID:"
read AZURE_SUBSCRIPTION_ID

echo "Enter the value for AZURE_TENANT:"
read AZURE_TENANT

echo "Enter the value for AZURE_CLIENT_ID:"
read AZURE_CLIENT_ID

echo "Enter the value for AZURE_SECRET:"
read -s AZURE_SECRET

echo "export AZURE_SUBSCRIPTION_ID=$AZURE_SUBSCRIPTION_ID" >> ~/.bashrc
echo "export AZURE_TENANT=$AZURE_TENANT" >> ~/.bashrc
echo "export AZURE_CLIENT_ID=$AZURE_CLIENT_ID" >> ~/.bashrc
echo "export AZURE_SECRET=$AZURE_SECRET" >> ~/.bashrc

echo "Environment variables set and added to .bashrc!"
```

### Usage

Open a terminal or command prompt.

Navigate to the directory where you saved the set_azure_env_vars.sh script.

Make the script executable by running the following command:

```bash
chmod +x set_azure_env_vars.sh

```
Execute the script by running the following command:

```bash
./set_azure_env_vars.sh
```

The script will prompt you to enter the values for each Azure environment variable:

```bash

AZURE_SUBSCRIPTION_ID: Enter your Azure subscription ID.
AZURE_TENANT: Enter your Azure tenant ID.
AZURE_CLIENT_ID: Enter your Azure client ID.
AZURE_SECRET: Enter your Azure secret (the input will be hidden for security purposes).
```

After entering all the values, the script will set the environment variables and append the corresponding export commands to your .bashrc file.
To apply the changes and make the environment variables available in the current shell session, run the following command:

```bash
source ~/.bashrc
```
The Azure environment variables are now set and will be available in future shell sessions.

### Security Considerations - WARNING

Keep your Azure secret value confidential and avoid sharing it or storing it in plain text.

Ensure that the set_azure_env_vars.sh script file has appropriate access permissions to prevent unauthorized access.

Consider using more secure methods, such as Azure Key Vault or other secret management solutions, for storing and managing sensitive credentials in a production environment. (coming soon)