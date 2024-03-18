from abc import ABC, abstractmethod


class Resource(ABC):
    """
    Represents a cloud resource across different cloud service providers (CSPs).

    Attributes:
        provider (str): The cloud service provider (CSP) where the VM is hosted.
        id (str): The unique identifier for the VM.
        region (str): The region where the VM is hosted.
    """

    def __init__(self, id, provider, region=None):
        self.id = id
        self.provider = provider
        self.region = region
        self.fetch_data()

    @abstractmethod
    def fetch_data(self):
        """
        Fetch resource data from the cloud provider.
        This method needs to be implemented by each subclass.
        """
        pass

    def to_dict(self):
        """
        Convert object to a dictionary, including nested objects
        that also have a to_dict method, but skipping private attributes
        (those starting with an underscore) and objects.
        """
        result = {}
        for key, value in self.__dict__.items():
            # Skip keys that start with an underscore
            if key.startswith('_'):
                continue

            if hasattr(value, 'to_dict') and callable(value.to_dict):
                # If the attribute is an object with a to_dict method, use it
                result[key] = value.to_dict()
            elif isinstance(value, list):
                # If the attribute is a list, iterate through its elements
                # Skip elements that are objects but do not have a to_dict method
                result[key] = [item.to_dict() if hasattr(item, 'to_dict') and callable(item.to_dict) else item for item
                               in value if not hasattr(item, '__dict__') or hasattr(item, 'to_dict')]
            elif not hasattr(value, '__dict__'):
                # Assign the value if it's not an object (doesn't have __dict__) or is explicitly allowed (like lists processed above)
                result[key] = value
        return result
