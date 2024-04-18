from azure.identity import ClientSecretCredential
from azure.mgmt.authorization import AuthorizationManagementClient
from azure.mgmt.subscription import SubscriptionClient

# Azure AD app and service principal details
tenant_id = "your_tenant_id"
client_id = "your_client_id"
client_secret = "your_client_secret"

# Subscription ID
subscription_id = "your_subscription_id"

# Create a credential object using the service principal details
credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret
)

# Create an AuthorizationManagementClient instance
authorization_client = AuthorizationManagementClient(credential, subscription_id)

# Create a SubscriptionClient instance
subscription_client = SubscriptionClient(credential)

# Get the subscription
subscription = next(subscription_client.subscriptions.list())

# Get the service principal object ID
sp_object_id = None
for sp in authorization_client.service_principals.list():
    if sp.app_id == client_id:
        sp_object_id = sp.object_id
        break

if sp_object_id:
    # Get the role assignments for the service principal
    role_assignments = authorization_client.role_assignments.list_for_scope(
        scope=f"/subscriptions/{subscription_id}",
        filter=f"principalId eq '{sp_object_id}'"
    )

    # Print the role assignments
    for assignment in role_assignments:
        role_definition = authorization_client.role_definitions.get_by_id(assignment.role_definition_id)
        print(f"Role: {role_definition.role_name}")
        print(f"Scope: {assignment.scope}")
        print(f"Principal ID: {assignment.principal_id}")
        print("---")
else:
    print("Service principal not found.")