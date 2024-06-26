import botocore.exceptions
from boto3 import client

from ....resources.obj_storage_container import ObjectStorageContainer


class AWSObjectStorageContainer(ObjectStorageContainer):
    def __init__(self, name, provider, region):
        self._client = client('s3')
        self.name = name
        self.provider = provider
        super().__init__(name=name, provider="aws", region=region)

    def fetch_data(self):
        """
        Fetch object storage container (S3 bucket) data from AWS.
        """

        # Get S3 Bucket Public Access Block Information
        self.all_public_access_blocked = True
        try:
            response = self._client.get_public_access_block(Bucket=self.name)
            for config_item in response['PublicAccessBlockConfiguration']:
                if response['PublicAccessBlockConfiguration'][config_item] is True:
                    continue
                else:
                    self.all_public_access_blocked = False
                    break
        except botocore.exceptions.ClientError: # handles case where 'Block All Public Access' is OFF
            self.all_public_access_blocked = False

        # Get Bucket Versioning and MFA Delete Status
        try:
            bucket_versioning_status = self._client.get_bucket_versioning(Bucket=self.name)['Status']

            if bucket_versioning_status == 'Enabled':
                self.versioning_enabled = True
            else:
                self.versioning_enabled = False

        except KeyError: # handles case where 'Bucket versioning' has never been turned on
            self.versioning_enabled = False
        
        try:
            mfa_delete_status = self._client.get_bucket_versioning(Bucket=self.name)['MFADelete']

            if mfa_delete_status == 'Enabled':
                self.provider_specific['MFADeleteEnabled'] = True
            else:
                self.provider_specific['MFADeleteEnabled'] = False

        except KeyError: # handles case where 'Bucket versioning' has never been turned on
            self.provider_specific['MFADeleteEnabled'] = False # Versioning has to be on for MFADelete to be active