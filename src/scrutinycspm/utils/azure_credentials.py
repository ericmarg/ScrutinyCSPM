import os
import json

def get_azure_credentials(azureProfilePath: str = "~/.azure/azureProfile.json") -> tuple:
    azure_profile_path = os.path.expanduser(azureProfilePath)
    
    if os.path.exists(azure_profile_path):
        with open(azure_profile_path, 'r') as file:
            azure_profile = json.load(file)
            
            subscriptions = azure_profile['subscriptions']
            if subscriptions:
                subscription_id = subscriptions[0]['id']
                tenant_id = subscriptions[0]['tenantId']
                
                return subscription_id, tenant_id
            else:
                print("No subscriptions found in the Azure profile.")
    else:
        print("Azure profile file not found.")
    
    return None, None

