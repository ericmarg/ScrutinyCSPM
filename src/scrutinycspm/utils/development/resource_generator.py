import boto3
from abc import ABC, abstractmethod
from src.scrutinycspm.resources.resource import Resource

def generate_resource_classes(resource_info, resource_type):
    resource_classes = {}

    for resource in resource_info:
        class_name = f"{resource_type}_{resource['id'].replace('-', '_')}"
        
        def __init__(self, id, provider, region=None, **kwargs):
            super(class_name, self).__init__(id, provider, region)
            for key, value in kwargs.items():
                setattr(self, key, value)
        
        def fetch_data(self):
            # Implement the fetch_data method for the specific resource type
            pass
        
        resource_class = type(class_name, (Resource,), {
            "__init__": __init__,
            "fetch_data": fetch_data,
            **resource
        })
        
        resource_classes[class_name] = resource_class

    return resource_classes