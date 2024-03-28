from unittest import TestCase, mock
from scrutinycspm.access.azure_iam import authenticate
from azure.identity import InteractiveBrowserCredential
from azure.mgmt.resource import ResourceManagementClient

class TestAzureIAM(TestCase):

    @mock.patch('scrutinycspm.access.azure_iam.InteractiveBrowserCredential')
    @mock.patch('scrutinycspm.access.azure_iam.ResourceManagementClient')
    def test_authenticate(self, mock_resource_client, mock_credential):
        # Mock the return values
        mock_credential.return_value = mock.Mock()
        mock_resource_client.return_value = mock.Mock()

        # Call the function under test
        subscription_id = "your_subscription_id"
        result = authenticate(subscription_id)

        # Assertions
        mock_credential.assert_called_once()
        mock_resource_client.assert_called_once_with(mock_credential.return_value, subscription_id)
        self.assertIsInstance(result, ResourceManagementClient)