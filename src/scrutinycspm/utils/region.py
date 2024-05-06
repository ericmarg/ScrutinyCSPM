import re

def find_aws_region(args):
    aws_regions = [
        "us-east-1", "us-east-2", "us-west-1", "us-west-2",
        "af-south-1", "ap-east-1", "ap-south-1", "ap-northeast-1",
        "ap-northeast-2", "ap-northeast-3", "ap-southeast-1", "ap-southeast-2",
        "ca-central-1", "eu-central-1", "eu-west-1", "eu-west-2",
        "eu-west-3", "eu-south-1", "eu-north-1", "me-south-1",
        "sa-east-1"
    ]

    for arg in args:
        if isinstance(arg, str):
            match = re.search(r"\b(" + "|".join(aws_regions) + r")\b", arg)
            if match:
                return match.group(1)

    return None