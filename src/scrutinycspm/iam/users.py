import boto3
from datetime import datetime


class UserResource:
    path: str = None
    username: str = None
    userid: str = None
    resource_name: str = None
    create_date: datetime = None
    password_last_used: datetime = None

    def __init__(self, region=None, path: str = None, username: str = None, userid: str = None, resource_name: str = None,
                 create_date: datetime = None, password_last_used: datetime = None):
        self.client = boto3.client('iam')
        self.path = path
        self.username = username
        self.userid = userid
        self.resource_name = resource_name
        self.create_date = create_date
        self.password_last_used = password_last_used

    def get_all_users(self):
        # Create a paginator
        paginator = self.client.get_paginator('list_users')

        # Create a PageIterator from the Paginator
        page_iterator = paginator.paginate()

        # Make a list of all users in the iterator contents
        users = list(page['Users'] for page in page_iterator)

        return users
