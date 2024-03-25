"""AWS Provider: Scan S3 Buckets"""

import json
import boto3
import botocore.exceptions
from opa_client.opa import OpaClient
from opa_client.errors import ConnectionsError

s3 = boto3.client('s3')
policy_directory = "policies/"

buckets_list = s3.list_buckets() # gathers all S3 buckets in target account
bucket_scan_dict = {}

# loops through all buckets, obtains Public Access Block and Versioning info for each
# Maps the appropriate AllPublicAccessBlocked and VersioningEnabled flags accordingly
for bucket in buckets_list['Buckets']:
    bucket_name = bucket['Name']

    bucket_properties = {}
    bucket_properties['AllPublicAccessBlocked'] = True

    try:
        response = s3.get_public_access_block(Bucket=bucket_name)
        for config_item in response['PublicAccessBlockConfiguration']:
            if response['PublicAccessBlockConfiguration'][config_item] is True:
                continue
            else:
                bucket_properties['AllPublicAccessBlocked'] = False
                break
    except botocore.exceptions.ClientError: # handles case where 'Block All Public Access' is OFF
        bucket_properties['AllPublicAccessBlocked'] = False

    try:
        bucket_versioning_status = s3.get_bucket_versioning(Bucket=bucket_name)['Status']
        if bucket_versioning_status == 'Enabled':
            bucket_properties['VersioningEnabled'] = True
        else:
            bucket_properties['VersioningEnabled'] = False
    except KeyError: # handles case where 'Bucket versioning' has never been turned on
        bucket_properties['VersioningEnabled'] = False
   
    bucket_scan_dict[bucket_name] = bucket_properties

print()
print('Bucket Scan report')
print(json.dumps(bucket_scan_dict))
print()
print('End of S3 Report\n')

# Tests connecting to OPA running in Server mode using OPA-python-client library
print('Connecting to OPA Server...')
opa = OpaClient()
try:
    print(opa.check_connection())
    opa.update_opa_policy_fromfile(filepath=f"{policy_directory}object_storage.rego", endpoint="obj_storage")
    for bucket in bucket_scan_dict:
        bucket_input_data = bucket_scan_dict[bucket]
        opa_result = opa.check_policy_rule(input_data=bucket_input_data, package_path='obj_storage', rule_name='obj_storage_container_compliant')
        print(f'Object Storage Container: {bucket}, Compliant: {opa_result}')  
except ConnectionsError:
    print("OPA Server Unreachable, please check to make sure OPA server is running.")
