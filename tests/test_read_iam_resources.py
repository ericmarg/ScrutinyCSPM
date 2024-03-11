import boto3
from src.scrutinycspm.iam import UserResource, Role, Policy
from pprint import pprint

console = boto3.session.Session(profile_name='default')
iam_console = console.resource('iam')


ur = UserResource()

users = ur.get_all_users()
for user in users:
    pprint(user)

role = Role()
roles = role.get_all_roles()
for r in roles:
    pprint(r)

policy = Policy()
policies = policy.get_all_policies()
for p in policies:
    pprint(p)