import boto3
import json

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

