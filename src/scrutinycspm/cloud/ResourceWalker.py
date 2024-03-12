from azure.identity import DefaultAzureCredential
from typing import Protocol, List

class ResourceInfo:
    def __init__(self, name: str, resource_type: str, location: str, resource_id: str):
        self.name = name
        self.type = resource_type
        self.location = location
        self.id = resource_id


class CloudResourceWalker(Protocol):
    def authenticate(self) -> None:
        """
        Authenticates with Azure using the appropriate credentials.
        """
        ...

    def walk_resources(self, subscription_id: str) -> List[ResourceInfo]:
        """
        Walks through all the resources in the specified Azure subscription.

        Args:
            subscription_id (str): The ID of the Azure subscription.

        Returns:
            List[ResourceInfo]: A list of ResourceInfo objects representing the resources in the subscription.
        """
        ...