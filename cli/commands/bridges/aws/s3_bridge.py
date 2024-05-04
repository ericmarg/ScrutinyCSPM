from opa_client.opa import OpaClient
from opa_client.errors import ConnectionsError
from src.scrutinycspm.providers.aws.resources.account import AWSAccount

def evaluate_object_storage_containers():
    new_account = AWSAccount()
    opa = OpaClient()

    for container in new_account.obj_storage_containers:
        container_dict = container.to_dict()  # formats the object model to a dict to be sent to OPA
        decisions = []

        # Attempts to evaluate all found Object Storage containers with three hardcoded Rego policies
        try:
            opa.update_opa_policy_fromfile(filepath="policies/object_storage.rego", endpoint="obj_storage")
            versioning_decision = opa.check_policy_rule(input_data=container_dict, package_path='obj_storage', rule_name='enforce_versioning_enabled')
            decisions.append(versioning_decision)
            public_access_block_decision = opa.check_policy_rule(input_data=container_dict, package_path='obj_storage', rule_name='enforce_public_access_block')
            decisions.append(public_access_block_decision)
            mfa_delete_decision = opa.check_policy_rule(input_data=container_dict, package_path='obj_storage', rule_name='enforce_aws_s3_mfa_enabled')
            decisions.append(mfa_delete_decision)

            print(f'Object Storage Container: {container.name}, Versioning Decision: {versioning_decision}, PublicBlock Decision: {public_access_block_decision}, MFADelete Decision: {mfa_delete_decision}')
            print()
            print("Remediations (if applicable):")
            print()
            print(f"Remediations for {container.name}")
            for decision in decisions:
                result = decision["result"]
                if result["status"] == "Not Compliant":
                    remediation_path = result["remediation_guidance"]
                    cloud_provider = result["provider"]
                    remediation_file = open(f"remediations/{cloud_provider}/{remediation_path}", "r")
                    remediation_file_contents = remediation_file.read()
                    print(remediation_file_contents)

        except ConnectionsError:  # Occurs when OPA is either not active or otherwise unreachable
            print("OPA Server Unreachable, please check to make sure OPA server is running.")