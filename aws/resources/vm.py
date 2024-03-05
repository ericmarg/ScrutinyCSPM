import boto3
from .security_group import SecurityGroup
class EC2Resource:
    def __init__(self, region=None):
        self.client = boto3.client('ec2', region_name=region)

    def get_all_instances(self):
        paginator = self.client.get_paginator('describe_instances')

        # Initialize a list to hold all instances
        all_instances = []

        # Iterate through pages
        for page in paginator.paginate():
            for reservation in page['Reservations']:
                for instance in reservation['Instances']:
                    security_groups = [SecurityGroup(sg['GroupId']) for sg in instance.get('SecurityGroups', [])]
                    volumes = instance.get('BlockDeviceMappings', [])
                    processed_volumes = []
                    for volume in volumes:
                        # Make sure 'Ebs' is present and then extract information
                        if 'Ebs' in volume:
                            processed_volumes.append({
                                'VolumeId': volume['Ebs'].get('VolumeId', 'N/A'),
                                'State': volume['Ebs'].get('Status', 'N/A'),
                            })

                    all_instances.append({
                        'InstanceId': instance['InstanceId'],
                        'InstanceType': instance['InstanceType'],
                        'State': instance['State']['Name'],
                        'PublicIpAddress': instance.get('PublicIpAddress', 'N/A'),
                        'PrivateIpAddress': instance.get('PrivateIpAddress', 'N/A'),
                        'VpcId': instance.get('VpcId', 'N/A'),
                        'SubnetId': instance.get('SubnetId', 'N/A'),
                        'SecurityGroups': security_groups,
                        'Tags': instance.get('Tags', []),
                        'Volumes': processed_volumes
                    })
        return all_instances