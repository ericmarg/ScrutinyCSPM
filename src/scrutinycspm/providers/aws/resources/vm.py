import boto3

from ....resources.virtual_machine import VirtualMachine


class VM(VirtualMachine):
    def __init__(self, id, provider, region):
        self._client = boto3.client('ec2', region_name=region)
        super().__init__(id, provider, region)

    def fetch_data(self):
        response = self._client.describe_instances(InstanceIds=[self.id])
        instance = response['Reservations'][0]['Instances'][0]
        self.name = instance.get('KeyName', 'N/A')
        self.state = instance['State']['Name']
        self.type = instance['InstanceType']
        self.status = instance['State']['Name']
        self.region = instance['Placement']['AvailabilityZone']