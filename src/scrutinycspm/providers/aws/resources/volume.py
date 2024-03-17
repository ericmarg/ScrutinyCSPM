from boto3 import client

from ....resources.volume import Volume


class AWSVolume(Volume):
    def __init__(self, id, region):
        self._client = client('ec2')
        super().__init__(id=id, provider="AWS", region=region)

    def fetch_data(self):
        """
        Fetch volume data from AWS.
        """
        response = self._client.describe_volumes(VolumeIds=[self.id])
        if response['Volumes']:
            volume = response['Volumes'][0]  # Assuming the ID uniquely identifies the volume
            self.name = volume.get('VolumeId')  # Optionally, use tags or other identifiers for name
            self.size = volume.get('Size')
            self.status = volume.get('State')
            self.attached_to = volume['Attachments'][0]['InstanceId'] if volume['Attachments'] else None
            # Populate provider_specific with any additional details
            self.provider_specific = {
                "SnapshotId": volume.get('SnapshotId'),
                "VolumeType": volume.get('VolumeType'),
                "CreateTime": volume.get('CreateTime').strftime('%Y-%m-%d %H:%M:%S')
            }
