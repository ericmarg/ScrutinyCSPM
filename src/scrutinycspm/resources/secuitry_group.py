from abc import ABC, abstractmethod

from .resource import Resource


class SecurityGroup(Resource, ABC):
    """
    Represents a Security Group across different cloud service providers (CSPs).

    Attributes:
        provider (str): The cloud service provider (CSP) where the Security Group is defined.
        id (str): The unique identifier for the Security Group.
        region (str): The region where the Security Group is defined.
        name (str): The name of the Security Group.
        description (str): The description of the Security Group.
        rules (list): The set of rules defined in the Security Group.
        provider_specific (dict): Provider-specific attributes and settings.
    """

    def __init__(self, id, provider, region):
        self.name = None
        self.description = None
        self.rules = []
        self.provider_specific = {}
        super().__init__(id, provider, region)

    @abstractmethod
    def fetch_data(self):
        """
        Fetch Security Group data from the cloud provider.
        This method needs to be implemented by each subclass.
        """
        pass
