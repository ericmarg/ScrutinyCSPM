import boto3
class Volume:
    def __init__(self, volume_id):
        self.volume_id = volume_id
        self.client = boto3.client('ec2')

    def get_details(self):
        response = self.client.describe_volumes(VolumeIds=[self.volume_id])
        return response['Volumes'][0]

    def to_dict(self):
        vol = self.get_details()
        return {
            'VolumeId': self.volume_id,
            'Size': vol.get('Size', 'N/A'),
            'State': vol.get('State', 'N/A'),
            'Encrypted': vol.get('Encrypted', 'N/A'),
        }