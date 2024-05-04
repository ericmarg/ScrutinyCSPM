def s3_bridge(self, bucket_versioning_status, all_public_access_blocked):
    """
    Fetch object storage container (S3 bucket) data from AWS.
    """

    # Set the all_public_access_blocked attribute based on the provided value
    self.all_public_access_blocked = all_public_access_blocked

    # Set the versioning_enabled attribute based on the provided bucket_versioning_status
    if bucket_versioning_status == 'Enabled':
        self.versioning_enabled = True
    else:
        self.versioning_enabled = False

    # Set the MFADeleteEnabled attribute based on the provided bucket_versioning_status
    if bucket_versioning_status == 'Enabled':
        try:
            mfa_delete_status = self._client.get_bucket_versioning(Bucket=self.name)['MFADelete']
            if mfa_delete_status == 'Enabled':
                self.provider_specific['MFADeleteEnabled'] = True
            else:
                self.provider_specific['MFADeleteEnabled'] = False
        except KeyError:
            self.provider_specific['MFADeleteEnabled'] = False
    else:
        self.provider_specific['MFADeleteEnabled'] = False