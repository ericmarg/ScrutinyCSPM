from boto3 import client

from ....resources.obj_storage_container import ObjectStorageContainer
import botocore.exceptions

class AWSObjectStorageContainer(ObjectStorageContainer):
    def __init__(self, name, provider, region):
        self._client = client('s3')
        self.name = name
        self.provider = provider
        super().__init__(id=id, provider="AWS", region=region)

    def fetch_data(self):
        """
        Fetch object storage container (S3 bucket) data from AWS.
        """
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

        try:
            bucket_versioning_status = self._client.get_bucket_versioning(Bucket=self.name)['Status']
            if bucket_versioning_status == 'Enabled':
                self.versioning_enabled = True
            else:
                self.versioning_enabled = False
        except KeyError: # handles case where 'Bucket versioning' has never been turned on
            self.versioning_enabled = False