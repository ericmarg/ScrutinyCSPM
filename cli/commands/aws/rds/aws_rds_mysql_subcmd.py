    # File: /home/robert/Documents/python_projects/recalitrant/ScrutinyCSPM/cli/commands/aws_rds_command.py


import json
from cli.commands.command_manager import SubCommandPlugin
from src.scrutinycspm.access.repository.github_provider import GitHubRepository
from src.scrutinycspm.resources.development.aws_rds_scan import RDSMySQLDatabaseRetriever
from src.scrutinycspm.utils.args import is_arg_present
from src.scrutinycspm.utils.aws_credential_file import get_aws_credentials
from src.scrutinycspm.utils.region import find_aws_region


class RDSMySQL(SubCommandPlugin):
    """
    Subcommand class for the 'rds-mysql' command.
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def execute(self, *args, **kwargs):
        """
        Executes the 'rds-mysql' command.
        """
        access_key, secret_key, profile_name = get_aws_credentials()
        region = find_aws_region(args)

        if region is None:
            return "Region not found", None

        print(f"Retrieving RDS, region: {region}...")
        rds = RDSMySQLDatabaseRetriever(region=region, access_key=access_key, secret_key=secret_key)
        json_data = rds.run_scan()
        data = json.loads(json_data)
        json_data = json.dumps(data, indent=4, sort_keys=True)

        if is_arg_present(args=args, arg_value="github"):
            github = GitHubRepository('robertfischer3/scrutiny-policies')
            policies = github.get_files_by_extension('storage', '.rego')
            for policy in policies:
                print(f"Policy group retrieved: {policy}")
                policy_content = github.get_file_contents(policy, 'main')
                print(policy_content)

        if is_arg_present(args=args, arg_value="scan"):
            print(f"Scanning RDS MySQL databases, region: {region}...")
            print("Not policies found for RDS MySQL databases. Feel free to contribute to the Scrutiny CSPM project on GitHub.")
            print("https://github.com/robertfischer3/scrutiny-policies")
            
        if is_arg_present(args=args, arg_value="verbose"):
            print(json_data)   
        
        if is_arg_present(args=args, arg_value="raw"):
            return json_data, None

        return "Scan completed", None