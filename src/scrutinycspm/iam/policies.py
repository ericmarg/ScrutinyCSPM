import boto3


class Policy:
    def __init__(self, region=None):
        self.client = boto3.client('iam')

    def get_all_policies(self):
        # Create a paginator
        paginator = self.client.get_paginator('list_policies')

        # Create a PageIterator from the Paginator
        page_iterator = paginator.paginate(OnlyAttached=False)

        # Make a list of all policies in the iterator contents
        policies = list(page['Policies'] for page in page_iterator)

        return policies
