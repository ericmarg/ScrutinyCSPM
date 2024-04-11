from azure.identity import InteractiveBrowserCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.identity import DefaultAzureCredential
from azure.identity import CertificateCredential
import logging
from typing import Dict, Any
from omegaconf import DictConfig, OmegaConf
from azure.identity import InteractiveBrowserCredential, ClientSecretCredential

class Azure_IAM_Provider:
    def __init__(self, log_config: DictConfig = OmegaConf.create(
        {"logging": {"level": {"AzureIAM_Provider": "ERROR"}}})):
        
        self.logger = logging.getLogger(__name__)

    def certificate_login(self, tenant_id: str, client_id: str, certificate_path: str) -> CertificateCredential:
        try:

            credential = CertificateCredential(
                tenant_id=tenant_id,
                client_id=client_id,
                certificate_path=certificate_path
            )

            return credential
            
        except Exception as e:
            self.logger.error(f"An error occurred while authenticating with certificate: {str(e)}")
            raise Exception(f"An error occurred while authenticating with certificate: {str(e)}") from e


    def interactive_login():
        try:
            # Create an instance of InteractiveBrowserCredential
            credential = InteractiveBrowserCredential()
            return credential
        except Exception as e:
            print(f"Error during interactive login: {str(e)}")
            return None


def main() -> int:
    # Azure subscription ID
    subscription_id = "6645551c-ec86-42a3-95bc-12f966b25d81"

    # Azure AD tenant ID
    tenant_id = "dd86d92c-82e6-4b30-b8f9-a065ba57bc0b"

    # Azure AD client ID
    client_id = "c589f1bd-4499-45de-adb8-cb89ff14371b"

    # Azure AD client secret
    certificate_path="/home/robert/tmp1_xf3jfr.pem"

    iam: Azure_IAM_Provider = Azure_IAM_Provider()
    
    # Authenticate using certificate login
    credential = iam.certificate_login(tenant_id, client_id, certificate_path)

    if credential is not None:
        # Get the resource inventory for the specified Azure subscription
        results = iam.get_azure_resource_inventory(tenant_id, subscription_id, credential)
        print(results)

    return 0


if __name__ == "__main__":
    main()
