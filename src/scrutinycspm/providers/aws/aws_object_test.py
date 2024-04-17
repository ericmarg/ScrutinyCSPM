from opa_client.opa import OpaClient
from opa_client.errors import ConnectionsError
from src.scrutinycspm.providers.aws.resources.account import AWSAccount

new_account = AWSAccount()
opa = OpaClient()

def format_decision(decision):
   if decision == {}:
      return "Compliant"
   else:
      return decision

for container in new_account.obj_storage_containers:
  # print(f"Name: {container.name}, PublicAccessBlocked: {container.all_public_access_blocked}, VersioningEnabled: {container.versioning_enabled} , MFADeleteEnabled: {container.provider_specific['MFADeleteEnabled']}")

  container_dict = container.to_dict()
  decisions = []
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
      if decision["result"]["status"] == "Not Compliant":
         remediation_path = decision["result"]["remediation_guidance"]
         remediation_file = open(f"remediations/{remediation_path}", "r")
         remediation_file_contents = remediation_file.read()
         print(remediation_file_contents)

      
  except ConnectionsError:
      print("OPA Server Unreachable, please check to make sure OPA server is running.")
