import boto3
class SecurityGroup:
    def __init__(self, group_id):
        self.group_id = group_id
        self.client = boto3.client('ec2')

    def get_details(self):
        response = self.client.describe_security_groups(GroupIds=[self.group_id])
        return response['SecurityGroups'][0]

    def formatRules(self, rule):
        return {
            'FromPort': rule.get('FromPort', 'N/A'),
            'ToPort': rule.get('ToPort', 'N/A'),
            'IpProtocol': rule.get('IpProtocol', 'N/A'),
            'IpRanges': rule.get('IpRanges', [])
        }

    def to_dict(self):
        sg = self.get_details()
        return {
            'GroupId': self.group_id,
            'GroupName': sg.get('GroupName', 'N/A'),
            'Inbound': list(map(self.formatRules,sg.get('IpPermissions', []))),
            'Outbound': list(map(self.formatRules, sg.get('IpPermissionsEgress', [])))
        }