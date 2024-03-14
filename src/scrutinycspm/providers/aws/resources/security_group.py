from boto3 import client

from ....resources.secuitry_group import SecurityGroup


class AWSSecurityGroup(SecurityGroup):
    def __init__(self, id, region):
        self._client = client('ec2')
        super().__init__(id=id, provider="AWS", region=region)

    def fetch_data(self):
        """
        Fetch security group data from AWS.
        """
        response = self._client.describe_security_groups(GroupIds=[self.id])
        if response['SecurityGroups']:
            sg = response['SecurityGroups'][0]  # Assuming the ID uniquely identifies the security group
            self.name = sg.get('GroupName')
            self.description = sg.get('Description')
            self.rules = self._parse_rules(sg.get('IpPermissions', []))
            # Populate provider_specific with any additional details
            self.provider_specific = {
                "VpcId": sg.get('VpcId'),
                "Tags": sg.get('Tags', [])
            }

    def _parse_rules(self, permissions):
        """
        Parse inbound rules from AWS format to a more generic format.
        """
        rules = []
        for permission in permissions:
            # Simplify and generalize the rule format
            rule = {
                "Protocol": permission['IpProtocol'],
                "FromPort": permission.get('FromPort'),
                "ToPort": permission.get('ToPort'),
                "IpRanges": [ip_range['CidrIp'] for ip_range in permission.get('IpRanges', [])]
            }
            rules.append(rule)
        return rules
