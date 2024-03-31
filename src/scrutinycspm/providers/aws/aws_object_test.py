from opa_client.opa import OpaClient
from opa_client.errors import ConnectionsError
from src.scrutinycspm.providers.aws.resources.account import AWSAccount

new_account = AWSAccount()
opa = OpaClient()
policy_directory = "policies/"

for container in new_account.obj_storage_containers:
  print(f"Name: {container.name}, PublicAccessBlocked: {container.all_public_access_blocked}, VersioningEnabled: {container.versioning_enabled} , MFADeleteEnabled: {container.provider_specific['MFADeleteEnabled']}")

  container_dict = container.to_dict()
  try:
    print(opa.check_connection())
    opa.update_opa_policy_fromfile(filepath=f"{policy_directory}object_storage.rego", endpoint="obj_storage")
    opa_result = opa.check_policy_rule(input_data=container_dict, package_path='obj_storage', rule_name='obj_storage_container_compliant')
    print(f'Object Storage Container: {container.name}, Compliant: {opa_result}')  
  except ConnectionsError:
      print("OPA Server Unreachable, please check to make sure OPA server is running.")
