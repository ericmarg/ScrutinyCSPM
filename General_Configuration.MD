# Configuration Files - README

This application utilizes two configuration files: `base-config.yaml` and `private_vault.yaml`. These files are essential for setting up and running the application properly.

## Notice:
<div style="background-color: #f0f0f0; padding: 10px;">
Additional configurations are also required in the current release of this application.

If you are running this code in a image container, these configurations need to be applied insider the container. 

### Preferred Method
[Configuring AWS and Azure Credentials for Scrutiny CSPM](docs/markdown/configuring_aws_azure_credentials.md)



### Alternative Methods
[Azure Environment Variables](docs/markdown/azure_environment_vars.md)

[AWS Credential File Script](docs/markdown/aws_credentials_script.md)

[AWS Credentials (Manual)](docs/markdown/aws_credentials.MD)

[Azure Enviromental Variables (manual)](docs/markdown/Azure_Authentication.MD)

</div>

## File Locations

1. `base-config.yaml`:
   - Location: `conf/base-config.yaml` (relative to the project's root)
   - This file serves as a template for the `private_vault.yaml` file.

2. `private_vault.yaml`:
   - Location: `conf/private/private_vault.yaml` (relative to the project's root)
   - This file contains the actual settings and sensitive information used by the application.
   - **Important**: This file is not checked into source control and must be created manually by the user.

## Configuration Steps

To properly configure the application, follow these steps:

1. Locate the `base-config.yaml` file in the `conf` folder.

2. Create a new folder named `private` inside the `conf` folder.

3. Copy the contents of `base-config.yaml` and create a new file named `private_vault.yaml` inside the `conf/private` folder.

4. Open the `private_vault.yaml` file and update the necessary settings:
   - Remove the `private_path` field as it is not required in the `private_vault.yaml` file.
   - Update the `hc_vault` section with the actual address, namespace, username, and password for the Vault server.
     - **Note**: The password field is sensitive and should be encrypted. Storing it in plain text is not recommended for production use.
   - Update the `azure_key_vault` section with the correct `tenant_id`, `client_id`, and `url` for your Azure Key Vault.
     - Set `certificate_authentication` to `true` if using certificate-based authentication.
     - Provide the correct path to the certificate file in the `certificate_path` field.
   - Update the `aws_secrets_manager` section with the actual `access_key_id`, `secret_access_key`, `session_token`, and `region` for your AWS Secrets Manager.
   - Update the `aws_credentials_file` section with the correct path to your AWS credentials file.
   - Update the `repositories` section with the necessary repository information and access tokens.
   - Update the `testing` section with the appropriate repository information, access tokens, and commit SHAs for testing.

5. Save the `private_vault.yaml` file.

## Important Considerations

- The `private_vault.yaml` file contains sensitive information and should never be checked into source control.
- Ensure that the `private_vault.yaml` file has appropriate access permissions and is only accessible to authorized users.
- When configuring the `hc_vault` section, it is strongly recommended to use secure methods for storing and handling the password, such as encryption or environment variables, instead of storing it in plain text.
- Make sure to update the necessary fields in the `private_vault.yaml` file with the correct values specific to your environment and setup.

By following these steps and configuring the `private_vault.yaml` file correctly, the application will be able to access the required settings and sensitive information securely.

If you have any further questions or need assistance with the configuration process, please contact the application's support team or refer to the application's documentation.

## Example:
Here's an example of how the `private_vault.yaml` file could be configured:

```yaml
secrets:
  hc_vault:
    address: https://vault-cluster-public-vault-example-only.hashicorp.cloud:8200
    namespace: admin/test_scrutinycspm
    username: robert1
    password: "encrypted_password"

  azure_key_vault:
    certificate_authentication: true
    certificate_path: /home/anypath/scrutinyexample.pem
    tenant_id: your_tenant_id
    client_id: your_client_id
    url: https://scrutinycspmvault01test.vault.azure.net/

  aws_secrets_manager:
    access_key_id: your_access_key_id
    secret_access_key: your_secret_access_key
    session_token: your_session_token
    region: us-east-2

  aws_credentials_file:
    path: ~/.aws/credentials

repositories:
  github:
    repository: your_repository
    token: your_token

testing:
  github:
    repository: your_testing_repository
    token: your_testing_token
    commits:
      - commit_sha1
      - commit_sha2
      - commit_sha3
    file_to_test: src/main.rs