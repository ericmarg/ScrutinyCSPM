from src.scrutinycspm.utils.development.resource_generator import generate_resource_classes
import boto3
import json

class EC2InstanceRetriever:
    def __init__(self, access_key, secret_key, region):
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.ec2_client = self.setup_ec2_client()

    def setup_ec2_client(self):
        return boto3.client(
            'ec2',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region
        )

    def get_ec2_instance_details(self, instance_id):
        instance_details = {}

        try:
            response = self.ec2_client.describe_instances(InstanceIds=[instance_id])
            instance = response['Reservations'][0]['Instances'][0]

            instance_details = {
                'InstanceId': instance['InstanceId'],
                'InstanceType': instance['InstanceType'],
                'State': instance['State']['Name'],
                'PublicIpAddress': instance.get('PublicIpAddress', ''),
                'PrivateIpAddress': instance.get('PrivateIpAddress', ''),
                'LaunchTime': instance['LaunchTime'].strftime('%Y-%m-%d %H:%M:%S'),
                'SecurityGroups': instance['SecurityGroups'],
                'IamInstanceProfile': instance.get('IamInstanceProfile', {}),
                'Tags': instance.get('Tags', [])
            }

        except Exception as e:
            print(f"Error retrieving details for instance '{instance_id}': {str(e)}")

        return instance_details

    def get_ec2_instances(self):
        try:
            response = self.ec2_client.describe_instances()
            instances = []

            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instance_id = instance['InstanceId']
                    instance_details = self.get_ec2_instance_details(instance_id)
                    instances.append(instance_details)

            return instances

        except Exception as e:
            print(f"Error retrieving EC2 instances: {str(e)}")
            return []

    def run_scan(self):
        instances = self.get_ec2_instances()
        scan_results = {
            'EC2Instances': instances
        }
        return json.dumps(scan_results, default=str)



