import boto3


class UserResource:
    def __init__(self, region=None):
        self.client = boto3.client('iam')

    def get_all_users(self):
        # Create a paginator
        paginator = self.client.get_paginator('list_users')

        # Create a PageIterator from the Paginator
        page_iterator = paginator.paginate()

        # Make a list of all users in the iterator contents
        users = list(page['Users'] for page in page_iterator)

        return users
