import json
import opa_client


def vulernabilities(configuration_data, endpoint:str, rego_policy:str): 

    # Create an OPA client
    opa = opa_client.OpaClient()
    opa.check_connection()

    opa.update_opa_policy_fromfile(filepath=rego_policy, endpoint=endpoint)
    print(opa.get_policies_info())

    # Evaluate the security configurations
    for configuration in configuration_data:
        result = opa.check_policy_rule(input_data=configuration, package_path=rego_policy, rule_name='enforce_security_configurations')
        if result.get('allow'):
            print(f"{endpoint} {configuration['name']} passed the security checks.")
        else:
            print(f"{endpoint} {configuration['name']} failed the security checks:")
            for msg in result.get('deny', []):
                print(f"  - {msg}")