import boto3


class Role:
    def __init__(self, region=None):
        self.client = boto3.client('iam')

    def get_all_roles(self):
        # Create a paginator
        paginator = self.client.get_paginator('list_roles')

        # Create a PageIterator from the Paginator
        page_iterator = paginator.paginate()

        # Make a list of all roles in the iterator contents
        roles = list(page['Roles'] for page in page_iterator)

        return roles
