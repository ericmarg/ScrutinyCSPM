from abc import ABC, abstractmethod

from .resource import Resource


class Volume(Resource, ABC):
    """
    Represents a block storage volume across different cloud service providers (CSPs).

    Attributes:
        provider (str): The cloud service provider (CSP) where the volume is provisioned.
        id (str): The unique identifier for the volume.
        region (str): The region where the volume is provisioned.
        name (str): The name of the volume.
        size (int): The size of the volume in GB.
        status (str): The status of the volume (e.g., available, in-use).
        attached_to (str): The ID of the VM to which the volume is attached, if any.
        provider_specific (dict): Provider-specific attributes and settings.
    """

    def __init__(self, id, provider, region):
        self.name = None
        self.size = None
        self.status = None
        self.attached_to = None
        self.provider_specific = {}
        super().__init__(id, provider, region)

    @abstractmethod
    def fetch_data(self):
        """
        Fetch volume data from the cloud provider.
        This method needs to be implemented by each subclass.
        """
        pass
