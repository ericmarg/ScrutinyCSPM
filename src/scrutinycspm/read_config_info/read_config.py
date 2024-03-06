import boto3
from distutils.command.config import config
import json
from botocore.exceptions import ClientError
from datetime import datetime

ACCOUNT_ID = '012345678901'
AGGREGATOR_NAME = 'my_aggregator'
REGION = 'us-east-1'
RESOURCE_TYPE = 'AWS::IAM::Group'

client = boto3.client('config')

# Create AWS Config aggregator
response = client.put_configuration_aggregator(
    ConfigurationAggregatorName=AGGREGATOR_NAME,
    AccountAggregationSources=[
        {
            'AccountIds': [
                ACCOUNT_ID,
            ],
            'AllAwsRegions': True,
            'AwsRegions': [
                REGION,
            ]
        },
    ],
    OrganizationAggregationSource={
        'RoleArn': 'string',
        'AwsRegions': [
            REGION,
        ],
        'AllAwsRegions': True
    },
    Tags=[
        {},
    ]
)

print(response)

# Describe aggregators
response = client.describe_configuration_aggregators(
    ConfigurationAggregatorNames=[
        AGGREGATOR_NAME,
    ],
    NextToken='',
    Limit=123
)

print(response)

# Return the current configuration items for resources that are present in the Config aggregator.
response = client.batch_get_aggregate_resource_config(
    ConfigurationAggregatorName=AGGREGATOR_NAME,
    ResourceIdentifiers=[
        {
            'SourceAccountId': ACCOUNT_ID,
            'SourceRegion': REGION,
            'ResourceId': 'string',
            'ResourceType': RESOURCE_TYPE,
            'ResourceName': 'string'
        },
    ]
)

print(response)