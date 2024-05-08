import boto3
import json

class AWSSecurityGroupScanner:
    def __init__(self, region, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.ec2_client = boto3.client('ec2', region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    def run_scan(self):
        security_groups = []

        try:
            # Retrieve all security groups in the specified region
            response = self.ec2_client.describe_security_groups()

            for group in response['SecurityGroups']:
                group_id = group['GroupId']
                group_name = group['GroupName']
                description = group['Description']
                vpc_id = group.get('VpcId', 'N/A')

                # Retrieve inbound rules
                inbound_rules = []
                for permission in group['IpPermissions']:
                    ip_protocol = permission['IpProtocol']
                    from_port = permission.get('FromPort', 'N/A')
                    to_port = permission.get('ToPort', 'N/A')

                    # Retrieve IP ranges for inbound rules
                    ip_ranges = [ip_range['CidrIp'] for ip_range in permission.get('IpRanges', [])]

                    # Retrieve security groups for inbound rules
                    security_group_ids = [sg['GroupId'] for sg in permission.get('UserIdGroupPairs', [])]

                    inbound_rule = {
                        'IpProtocol': ip_protocol,
                        'FromPort': from_port,
                        'ToPort': to_port,
                        'IpRanges': ip_ranges,
                        'SecurityGroupIds': security_group_ids
                    }
                    inbound_rules.append(inbound_rule)

                # Retrieve outbound rules (similar to inbound rules)
                outbound_rules = []
                for permission in group['IpPermissionsEgress']:
                    ip_protocol = permission['IpProtocol']
                    from_port = permission.get('FromPort', 'N/A')
                    to_port = permission.get('ToPort', 'N/A')

                    ip_ranges = [ip_range['CidrIp'] for ip_range in permission.get('IpRanges', [])]
                    security_group_ids = [sg['GroupId'] for sg in permission.get('UserIdGroupPairs', [])]

                    outbound_rule = {
                        'IpProtocol': ip_protocol,
                        'FromPort': from_port,
                        'ToPort': to_port,
                        'IpRanges': ip_ranges,
                        'SecurityGroupIds': security_group_ids
                    }
                    outbound_rules.append(outbound_rule)

                security_group = {
                    'GroupId': group_id,
                    'GroupName': group_name,
                    'Description': description,
                    'VpcId': vpc_id,
                    'InboundRules': inbound_rules,
                    'OutboundRules': outbound_rules
                }
                security_groups.append(security_group)

        except Exception as e:
            print(f"Error scanning security groups: {str(e)}")

        return json.dumps(security_groups, indent=4)