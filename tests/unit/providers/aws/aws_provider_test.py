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

boto3_mock.client.return_value.get_caller_identity.return_value = AWS_DATA['get_caller_identity']
boto3_mock.client.return_value.get_paginator.return_value.paginate.return_value = dict(AWS_DATA['describe_instances'])

account = AWSAccount()

class TestAWSAccount(unittest.TestCase):
    def test_aws_account(self):
        self.assertEqual(account.id, AWS_DATA['get_caller_identity']['Account'])

    def test_get_vms(self):
        self.assertEqual(len(account.vms), 1)
        self.assertEqual(account.vms[0].id, AWS_DATA['describe_instances']['Reservations'][0]['Instances'][0]['InstanceId'])

if __name__ == '__main__':
    unittest.main()
