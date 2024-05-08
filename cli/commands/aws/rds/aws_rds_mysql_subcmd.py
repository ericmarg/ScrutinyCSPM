    # File: /home/robert/Documents/python_projects/recalitrant/ScrutinyCSPM/cli/commands/aws_rds_command.py


from cli.commands.command_manager import SubCommandPlugin
from src.scrutinycspm.providers.azure.policy_check import vulernabilities
from src.scrutinycspm.resources.development.aws_rds_scan import RDSMySQLDatabaseRetriever
from src.scrutinycspm.utils.aws_credential_file import get_aws_credentials


class RDSMySQL(SubCommandPlugin):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def execute(self, *args, **kwargs):
        access_key, secret_key, profile_name = get_aws_credentials()
        region = args[1]
        rds = RDSMySQLDatabaseRetriever(region=region, access_key=access_key, secret_key=secret_key)
        json_data = rds.run_scan()

        if len(args) > 0 and args[0] == 'table':
            return rds.format_rds_data(json_data)

        if len(args) > 0 and args[0] == 'scan':
            vulernabilities_json_data = vulernabilities(json_data, "obj_storage", "policies/object_storage.rego")

            return json_data, vulernabilities_json_data
        return json_data, None