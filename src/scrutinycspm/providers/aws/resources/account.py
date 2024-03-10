import boto3

from ....resources.cloud_account import CloudAccount
from .vm import VM


def get_account_id():
    client = boto3.client('sts')
    return client.get_caller_identity()['Account']


class AWSAccount(CloudAccount):
    def __init__(self, region=None):
        self.id = get_account_id()
        super().__init__(self.id, 'AWS', region)
        self.fetch_data(region)

    def fetch_data(self, region=None):
        self.vms = self.get_vms(region)

    def get_vms(self, region):
        client = boto3.client('ec2', region_name=region)
        paginator = client.get_paginator('describe_instances')
        # Initialize a list to hold all instances
        all_instances = []
        # Iterate through pages
        for page in paginator.paginate():
            for reservation in page['Reservations']:
                for instance in reservation['Instances']:
                    all_instances.append(VM(instance['InstanceId'], self.provider, self.region))
        return all_instances
