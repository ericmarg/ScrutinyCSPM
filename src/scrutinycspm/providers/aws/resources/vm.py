import boto3

from .security_group import AWSSecurityGroup
from .volume import AWSVolume
from ....resources.virtual_machine import VirtualMachine


class VM(VirtualMachine):
    def __init__(self, id, provider, region):
        if region:
            self._client = boto3.client('ec2', region_name=region)
        else:
            self._client = boto3.client('ec2')
        super().__init__(id, provider, region)

    def fetch_data(self):
        response = self._client.describe_instances(InstanceIds=[self.id])
        instance = response['Reservations'][0]['Instances'][0]
        self.name = instance.get('KeyName', 'N/A')
        self.state = instance['State']['Name']
        self.type = instance['InstanceType']
        self.status = instance['State']['Name']

        volumes = []

        for mapping in instance.get('BlockDeviceMappings', []):
            volume_id = mapping['Ebs']['VolumeId']
            aws_volume = AWSVolume(volume_id, region=self.region)
            try:
                aws_volume.fetch_data()
                volumes.append(aws_volume)
            except Exception as e:
                print(f"Failed to fetch volume data for {volume_id}: {e}")

        self.volumns = volumes

        security_groups = []

        for sg in instance.get('SecurityGroups', []):
            aws_sg = AWSSecurityGroup(sg['GroupId'], region=self.region)

            try:
                aws_sg.fetch_data()
                security_groups.append(aws_sg)
            except Exception as e:
                print(f"Failed to fetch security group data for {sg_id}: {e}")

        self.security_groups = security_groups
