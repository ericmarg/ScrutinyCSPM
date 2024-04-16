from opa_client.opa import OpaClient
from opa_client.errors import ConnectionsError
from src.scrutinycspm.providers.aws.resources.account import AWSAccount

new_account = AWSAccount()
opa = OpaClient()
policy_directory = "policies/"

def format_decision(decision):
   if decision == {}:
      return "Compliant"
   else:
      return decision

for container in new_account.obj_storage_containers:
  # print(f"Name: {container.name}, PublicAccessBlocked: {container.all_public_access_blocked}, VersioningEnabled: {container.versioning_enabled} , MFADeleteEnabled: {container.provider_specific['MFADeleteEnabled']}")

  container_dict = container.to_dict()
  try:
    opa.update_opa_policy_fromfile(filepath=f"{policy_directory}object_storage.rego", endpoint="obj_storage")
    versioning_decision = opa.check_policy_rule(input_data=container_dict, package_path='obj_storage', rule_name='enforce_versioning_enabled')
    public_access_block_decision = opa.check_policy_rule(input_data=container_dict, package_path='obj_storage', rule_name='enforce_public_access_block')
    mfa_delete_decision = opa.check_policy_rule(input_data=container_dict, package_path='obj_storage', rule_name='enforce_aws_s3_mfa_enabled')
    print(f'Object Storage Container: {container.name}, Versioning Decision: {format_decision(versioning_decision)}, PublicBlock Decision: {format_decision(public_access_block_decision)}, MFADelete Decision: {format_decision(mfa_delete_decision)}')
    print()

  except ConnectionsError:
      print("OPA Server Unreachable, please check to make sure OPA server is running.")
