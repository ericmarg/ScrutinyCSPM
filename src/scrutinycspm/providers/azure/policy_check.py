import subprocess
import opa_client
import requests

class OPAPolicyEval:
    def __init__(self):
        self.client = opa_client.OpaClient()

    def start_opa_server(self):
        try:
            # Check if the OPA server is already running
            if self.is_opa_server_running():
                print("OPA server is already running.")
                return

            # Start the OPA server using the subprocess module
            opa_process = subprocess.Popen(["opa", "run", "-s"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Wait for the server to start (you can adjust the timeout if needed)
            opa_process.wait(timeout=5)

            # Check the server's status
            if opa_process.poll() is None:
                print("OPA server started successfully.")
            else:
                print("Failed to start OPA server.")
                stderr_output = opa_process.stderr.read().decode()
                print("Error output:", stderr_output)

        except FileNotFoundError:
            print("OPA binary not found. Make sure OPA is installed and accessible from the PATH.")

        except subprocess.TimeoutExpired:
            print("Timeout occurred while starting the OPA server.")

        except Exception as e:
            print("An error occurred while starting the OPA server:", str(e))

    def is_opa_server_running(self):
        try:
            # Check if the OPA server is running by sending a request to the health endpoint
            response = requests.get("http://localhost:8181/health")
            return response.status_code == 200
        except requests.ConnectionError:
            return False
            
    def check_connection(self):
        self.client.check_connection()

    def update_opa_policy_fromfile(self, filepath, endpoint):
        self.client.update_opa_policy_fromfile(filepath=filepath, endpoint=endpoint)

    def get_policies_info(self):
        return self.client.get_policies_info()

    def check_policy_rule(self, input_data, package_path, rule_name):
        return self.client.check_policy_rule(input_data=input_data, package_path=package_path, rule_name=rule_name)

def vulernabilities(configuration_data, endpoint: str, rego_policy: str):
    # Create an OPA client
    opa = OPAPolicyEval()

    # Start the OPA server
    opa.start_opa_server()

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
                print(f" - {msg}")