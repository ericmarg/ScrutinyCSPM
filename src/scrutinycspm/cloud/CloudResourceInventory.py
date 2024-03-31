from typing import Protocol, List

class ResourceInfo:
    def __init__(self, name: str, resource_type: str, location: str, resource_id: str):
        self.name = name
        self.type = resource_type
        self.location = location
        self.id = resource_id


class CloudResourceInventory(Protocol):
    def authenticate(self, credential) -> None:
        """
        Authenticates using the appropriate credentials.
        """
        ...

    def get_resource_inventory(self, account_id: str) -> List[ResourceInfo]:
        """
        Walks through all the resources in the specified subscription/account.

        Args:
            account_id (str): The ID of the subscription/account.

        Returns:
            List[ResourceInfo]: A list of ResourceInfo objects representing the resources in the subscription/account.
        """
        ...