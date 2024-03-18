from abc import ABC, abstractmethod

from .resource import Resource


class ObjectStorageContainer(Resource, ABC):
    """
    Represents an object storage container (Examples: AWS S3 Bucket, Azure Blob Storage Container) across different cloud service providers (CSPs).

    Attributes:
        provider (str): The cloud service provider (CSP) where the object storage container is provisioned.
        name (str): The unique identifier for the object storage container.
        region (str): The region where the container is provisioned.
        provider_specific (dict): Provider-specific attributes and settings.
    """

    def __init__(self, name, provider, region):
        self.name = name
        self.region = region
        self.provider = provider
        self.all_public_access_blocked = None
        self.versioning_enabled = None
        self.provider_specific = {}
        super().__init__(id, provider, region)

    @abstractmethod
    def fetch_data(self):
        """
        Fetch volume data from the cloud provider.
        This method needs to be implemented by each subclass.
        """
        pass
