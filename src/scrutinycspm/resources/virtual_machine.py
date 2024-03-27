from abc import ABC, abstractmethod

from .resource import Resource


class VirtualMachine(Resource, ABC):
    """
    Represents a Virtual Machine (VM) across different cloud service providers (CSPs).

    Attributes:
        provider (str): The cloud service provider (CSP) where the VM is hosted.
        id (str): The unique identifier for the VM.
        region (str): The region where the VM is hosted.
        name (str): The name of the VM.
        state (str): The state of the VM.
        type (str): The type or size of the VM.
        status (str): The status of the VM (e.g., running, stopped).
        public_ip (str): The public IP address of the VM.
        provider_specific (dict): Provider-specific attributes and settings.

        volumes (list(Volume)): The set of volumes attached to the VM.
        security_groups (list(SecurityGroup)): The set of security groups associated with the VM.
    """

    def __init__(self, id, provider, region):
        self.name = None
        self.state = None
        self.type = None
        self.region = None
        self.status = None
        self.volumes = []
        self.security_groups = []
        self.public_ip = None
        self.provider_specific = {}
        super().__init__(id, provider, region)

    @abstractmethod
    def fetch_data(self):
        """
        Fetch VM data from the cloud provider.
        This method needs to be implemented by each subclass.
        """
        pass
