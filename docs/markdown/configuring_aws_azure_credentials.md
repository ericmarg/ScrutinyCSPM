# Configuring AWS and Azure Credentials for Scrutiny CSPM

This document explains how to configure the AWS and Azure credentials for the Scrutiny CSPM (Cloud Security Posture Management) tool using a .env file and the docker-compose.yml configuration.
## AWS Credentials

To configure AWS credentials for Scrutiny CSPM, you need to provide the AWS access key ID and secret access key. These credentials are typically stored in the ~/.aws/credentials file on your local machine.
.aws/credentials File Format

The ~/.aws/credentials file should have the following format:

[default]
aws_access_key_id = <your access key id>
aws_secret_access_key = <your secret access key>

Replace <your access key id> with your actual AWS access key ID and <your secret access key> with your AWS secret access key.
Mounting AWS Credentials in Docker Compose

To make the AWS credentials available to the Scrutiny CSPM container, you need to mount the ~/.aws directory from your local machine to the container. This is achieved using the volumes section in the docker-compose.yml file:

### yaml

volumes:
  - ~/.aws:/root/.aws

This mounts the ~/.aws directory from your local machine to the /root/.aws directory inside the container.

## Azure Credentials

To configure Azure credentials for Scrutiny CSPM, you need to provide the Azure subscription ID, tenant ID, client ID, and secret. These credentials are stored in the .env file.
.env File Format

The .env file should have the following format:

AZURE_SUBSCRIPTION_ID=<your subscription id>
AZURE_TENANT=<your tenant id>
AZURE_CLIENT_ID=<your client id>
AZURE_SECRET=<your secret>

Replace <your subscription id>, <your tenant id>, <your client id>, and <your secret> with your actual Azure credentials.
Using Azure Credentials in Docker Compose

To make the Azure credentials available to the Scrutiny CSPM container, you need to specify the .env file in the docker-compose.yml configuration using the env_file section:

### yaml

env_file:
  - .env

This loads the environment variables defined in the .env file and makes them available to the container.
Running Scrutiny CSPM with Configured Credentials

With the AWS and Azure credentials properly configured, you can run Scrutiny CSPM using the docker-compose.yml file:

docker-compose up -d

This command starts the Scrutiny CSPM container and the Open Policy Agent (OPA) container defined in the docker-compose.yml file. The AWS and Azure credentials will be available to the Scrutiny CSPM container based on the configured .aws/credentials file and .env file.

Make sure to keep your credentials secure and do not commit the .env file or the ~/.aws/credentials file to version control systems.
