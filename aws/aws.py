from resources.vm import EC2Resource
import json

def default_serializer(obj):
    # Check if the object has a to_dict method and call it
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    # Raise a TypeError if the object is not serializable
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

if __name__ == '__main__':
    ec2 = EC2Resource()
    instances = ec2.get_all_instances()
    print(json.dumps(instances, indent=4, default=default_serializer))