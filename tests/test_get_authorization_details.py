import boto3
from src.scrutinycspm.iam import *
from pprint import pprint

console = boto3.session.Session(profile_name='default')
iam_console = console.resource('iam')

account = Account()

account_details = account.get_account_authorization_details()
pprint(account_details)