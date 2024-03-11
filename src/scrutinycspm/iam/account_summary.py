import boto3


class AccountSummary:
    def __init__(self, region=None):
        self.client = boto3.client('iam')

    def get_acocunt_summary(self):
        try:
            response = self.client.get_account_summary()
            return response
        except self.client.exceptions.ServiceFailureException:
            return None

