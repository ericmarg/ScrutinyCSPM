from opa_client.opa import OpaClient
from opa_client.errors import ConnectionsError
from src.scrutinycspm.providers.aws.resources.account import AWSAccount
import json
import jmespath

def evaluate_object_storage_containers(containers, repository: str=None) -> None:
    
    opa = OpaClient()

    for container in containers:

        decisions = []

        # Attempts to evaluate all found Object Storage containers with three hardcoded Rego policies
        try:
            if repository:
                opa.update_opa_policy_fromfile(
                    filepath="policies/object_storage.rego", endpoint="obj_storage"
                )   
            else:
                opa.update_opa_policy_fromfile(
                    filepath="policies/object_storage.rego", endpoint="obj_storage"
                )
            versioning_decision = opa.check_policy_rule(
                input_data=container,
                package_path="obj_storage",
                rule_name="enforce_versioning_enabled",
            )
            decisions.append(versioning_decision)
            public_access_block_decision = opa.check_policy_rule(
                input_data=container,
                package_path="obj_storage",
                rule_name="enforce_public_access_block",
            )
            decisions.append(public_access_block_decision)
            mfa_delete_decision = opa.check_policy_rule(
                input_data=container,
                package_path="obj_storage",
                rule_name="enforce_aws_s3_mfa_enabled",
            )
            decisions.append(mfa_delete_decision)

            name = container["name"]

            print(
                f"Object Storage Container: {name}, \nVersioning Decision: {versioning_decision}, \nPublicBlock Decision: {public_access_block_decision}, \nMFADelete Decision: {mfa_delete_decision}"
            )
            print()
            print("Remediations (if applicable):")
            print()
            print(f"Remediations for {name}")
            for decision in decisions:
                result = decision["result"]
                if result["status"] == "Not Compliant":
                    remediation_path = result["remediation_guidance"]
                    cloud_provider = result["provider"]
                    remediation_file = open(
                        f"remediations/{cloud_provider}/{remediation_path}", "r"
                    )
                    remediation_file_contents = remediation_file.read()
                    print(remediation_file_contents)

        except (
            ConnectionsError
        ):  # Occurs when OPA is either not active or otherwise unreachable
            print(
                "OPA Server Unreachable, please check to make sure OPA server is running."
            )


def s3_transformation(json_content):
    # Parse the JSON content
    data = json.loads(json_content)

    s3_dict = []

    for bucket in data['S3Buckets']:
        # Retrieve the bucket details
        bucket_name = bucket["Name"]
        provider = "aws"

        ignore_pub_acl = bucket.get("Details", {}).get("PublicAccessBlock", {}).get("IgnorePublicAcls", False)
        restrict_pub_bucket = bucket.get("Details", {}).get("PublicAccessBlock", {}).get("RestrictPublicBuckets", False)
        block_pub_acl = bucket.get("Details", {}).get("PublicAccessBlock", {}).get("BlockPublicAcls", False)
        block_pub_pol = bucket.get("Details", {}).get("PublicAccessBlock", {}).get("BlockPublicPolicy", False)

        versioning_enabled = bucket["Details"]["Versioning"] or False
        location = bucket.get("Details", {}).get("Location", "Error")

        # Create a dictionary to store the S3 bucket details
        s3_dict_item = {
            "name": bucket_name,
            "provider": provider,
            "region": location, # Location is the region
            "all_public_access_blocked": ignore_pub_acl and restrict_pub_bucket and block_pub_acl and block_pub_pol,
            "versioning_enabled": versioning_enabled,
            "provider_specific": {'MFADeleteEnabled': False},
            "id": bucket_name
        }

        s3_dict.append(s3_dict_item)


    return s3_dict