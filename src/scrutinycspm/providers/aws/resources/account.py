import boto3

from .obj_storage_container import AWSObjectStorageContainer as ObjectStorageContainer
from .vm import VM
from ....resources.cloud_account import CloudAccount


def get_account_id():
    client = boto3.client('sts')
    return client.get_caller_identity()['Account']


class AWSAccount(CloudAccount):
    def __init__(self, region=None):
        self.id = get_account_id()
        self.region = region
        super().__init__(self.id, 'AWS', self.region)


    def fetch_data(self):
        self.vms = self.get_vms()
        self.obj_storage_containers = self.get_obj_storage_containers()


    def get_vms(self):
        client = boto3.client('ec2')
        if self.region:
            client = boto3.client('ec2', region_name=self.region)
        paginator = client.get_paginator('describe_instances')
        # Initialize a list to hold all instances
        all_instances = []
        # Iterate through pages
        for page in paginator.paginate():
            for reservation in page['Reservations']:
                for instance in reservation['Instances']:
                    all_instances.append(VM(instance['InstanceId'], self.provider, self.region))
        return all_instances

    def get_obj_storage_containers(self):
        client = boto3.client('s3')
        buckets = client.list_buckets()
        # Initialize a list to hold all S3 buckets
        all_buckets = []
        for bucket in buckets['Buckets']:
            all_buckets.append(AWSObjectStorageContainer(bucket['Name'], self.provider, self.region))
        return all_buckets
