import boto3
import json

import tabulate

class RDSMySQLDatabaseRetriever:
    def __init__(self, access_key, secret_key, region):
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.rds_client = self.setup_rds_client()

    def setup_rds_client(self):
        return boto3.client(
            'rds',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region
        )

    def get_rds_mysql_database_details(self, db_instance_identifier):
        database_details = {}

        try:
            response = self.rds_client.describe_db_instances(DBInstanceIdentifier=db_instance_identifier)
            db_instance = response['DBInstances'][0]

            database_details = {
                'DBInstanceIdentifier': db_instance['DBInstanceIdentifier'],
                'Engine': db_instance['Engine'],
                'EngineVersion': db_instance['EngineVersion'],
                'DBInstanceClass': db_instance['DBInstanceClass'],
                'AllocatedStorage': db_instance['AllocatedStorage'],
                'StorageType': db_instance['StorageType'],
                'MultiAZ': db_instance['MultiAZ'],
                'PubliclyAccessible': db_instance['PubliclyAccessible'],
                'Endpoint': db_instance['Endpoint'],
                'VpcSecurityGroups': db_instance['VpcSecurityGroups'],
                'InstanceCreateTime': db_instance['InstanceCreateTime'].strftime('%Y-%m-%d %H:%M:%S'),
                'BackupRetentionPeriod': db_instance['BackupRetentionPeriod'],
                'EncryptionEnabled': db_instance.get('StorageEncrypted', False),
                'IAMDatabaseAuthenticationEnabled': db_instance['IAMDatabaseAuthenticationEnabled']
            }

        except Exception as e:
            print(f"Error retrieving details for database '{db_instance_identifier}': {str(e)}")

        return database_details

    def get_rds_mysql_databases(self):
        try:
            response = self.rds_client.describe_db_instances(
                Filters=[
                    {
                        'Name': 'engine',
                        'Values': ['mysql']
                    }
                ]
            )
            databases = []

            for db_instance in response['DBInstances']:
                db_instance_identifier = db_instance['DBInstanceIdentifier']
                database_details = self.get_rds_mysql_database_details(db_instance_identifier)
                databases.append(database_details)

            return databases

        except Exception as e:
            print(f"Error retrieving RDS MySQL databases: {str(e)}")
            return []

    def run_scan(self):
        databases = self.get_rds_mysql_databases()
        scan_results = {
            'RDSMySQLDatabases': databases
        }
        return json.dumps(scan_results, default=str)

    def format_rds_data(self, rds_data):
        try:
            rds_databases = json.loads(rds_data)["RDSMySQLDatabases"]
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing JSON data: {str(e)}")
            return None

        headers = ["DB Instance Identifier", "Engine", "Engine Version", "Instance Class", "Allocated Storage",
                "Storage Type", "Multi-AZ", "Publicly Accessible", "Endpoint Address", "Endpoint Port",
                "Endpoint Hosted Zone ID", "VPC Security Group ID", "Security Group Status", "Instance Create Time",
                "Backup Retention Period", "Encryption Enabled", "IAM DB Authentication Enabled"]

        data = []
        for db in rds_databases:
            try:
                endpoint = db["Endpoint"]
                vpc_security_group = db["VpcSecurityGroups"][0]
                data.append([
                    db.get("DBInstanceIdentifier", "N/A"),
                    db.get("Engine", "N/A"),
                    db.get("EngineVersion", "N/A"),
                    db.get("DBInstanceClass", "N/A"),
                    db.get("AllocatedStorage", "N/A"),
                    db.get("StorageType", "N/A"),
                    db.get("MultiAZ", "N/A"),
                    db.get("PubliclyAccessible", "N/A"),
                    endpoint.get("Address", "N/A"),
                    endpoint.get("Port", "N/A"),
                    endpoint.get("HostedZoneId", "N/A"),
                    vpc_security_group.get("VpcSecurityGroupId", "N/A"),
                    vpc_security_group.get("Status", "N/A"),
                    db.get("InstanceCreateTime", "N/A"),
                    db.get("BackupRetentionPeriod", "N/A"),
                    db.get("EncryptionEnabled", "N/A"),
                    db.get("IAMDatabaseAuthenticationEnabled", "N/A")
                ])
            except (KeyError, IndexError) as e:
                print(f"Error extracting data for RDS database: {str(e)}")
                continue

        if not data:
            print("No valid RDS databases found in the JSON data.")
            return None

        try:
            table = tabulate(data, headers, tablefmt="grid")
            return table
        except Exception as e:
            print(f"Error creating the table: {str(e)}")
            return None