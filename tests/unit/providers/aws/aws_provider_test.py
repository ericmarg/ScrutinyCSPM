import unittest
from unittest.mock import MagicMock, patch
import json
from src.scrutinycspm.providers.aws.resources.account import AWSAccount

boto3_mock = MagicMock()
boto3_client_mock = boto3_mock.client
patcher = patch('boto3.client', boto3_client_mock)
patcher.start()

with open('./aws.json') as f:
    AWS_DATA = json.load(f)
class TestAWSAccount(unittest.TestCase):
    def test_aws_account(self):
        boto3_mock.client.return_value.get_caller_identity.return_value = AWS_DATA['get_caller_identity']

        account = AWSAccount()

        self.assertEqual(account.id, AWS_DATA['get_caller_identity']['Account'])

if __name__ == '__main__':
    unittest.main()
