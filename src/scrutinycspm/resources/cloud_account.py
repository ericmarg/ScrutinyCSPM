from abc import ABC, abstractmethod

from .resource import Resource


class CloudAccount(Resource, ABC):
    """
    Represents a cloud account across different cloud service providers (CSPs).

    Attributes:
        provider (str): The cloud service provider (CSP) where the VM is hosted.
        id (str): The unique identifier for the VM.
        vms (list): A list of VMs in the cloud account.
        obj_storage_containers (list): A list of object storage containers in the cloud account.
    """

    def __init__(self, id, provider, region):
        super().__init__(id, provider, region)
        self.vms = []
        self.obj_storage_containers = []
        self.fetch_data()

    @abstractmethod
    def fetch_data(self):
        """
        Fetch cloud account data from the cloud provider.
        This method needs to be implemented by each subclass.
        """
        pass
