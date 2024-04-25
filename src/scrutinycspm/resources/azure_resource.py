from typing import Protocol

class AzureResource(Protocol):
    """
    Represents an Azure resource.

    Attributes:
        subscription_id (str): The subscription ID for the Azure resource.
        tenant_id (str): The tenant ID for the Azure resource.
        client_id (str): The client ID for accessing the Azure resource.
        client_secret (str): The client secret for accessing the Azure resource.
        client_certificate (str): The client certificate for accessing the Azure resource.
    """

    subscription_id: str
    tenant_id: str
    client_id: str
    client_secret: str
    client_certificate: str

    def fetch_data(self) -> None:
        """
        Fetch resource data from Azure.

        This method needs to be implemented by each subclass.
        """
        ...

    def to_dict(self) -> dict:
        """
        Convert the resource object to a dictionary.

        Returns:
            dict: A dictionary representation of the resource object.
        """
        result = {}
        for key, value in self.__dict__.items():
            if key.startswith('_'):
                continue
            if hasattr(value, 'to_dict') and callable(value.to_dict):
                result[key] = value.to_dict()
            elif isinstance(value, list):
                result[key] = [item.to_dict() if hasattr(item, 'to_dict') and callable(item.to_dict) else item
                               for item in value if not hasattr(item, '__dict__') or hasattr(item, 'to_dict')]
            elif not hasattr(value, '__dict__'):
                result[key] = value
        return result