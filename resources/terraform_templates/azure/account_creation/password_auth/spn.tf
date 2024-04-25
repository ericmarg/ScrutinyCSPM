# Configure the Azure provider
provider "azurerm" {
  features {}
}

# Create a resource group
resource "azurerm_resource_group" "scrutiny_rg_101" {
  name     = "scrutiny_rg_101"
  location = "eastus"
}

resource "azurerm_resource_group" "scrutiny_storage_rg" {
  name     = "scrutiny_storage_rg_101"
  location = "eastus"
  
}
# Create an Azure AD Application
resource "azuread_application" "scrutiny_app_101" {
  display_name = "Scrutiny Azure App 101"  # Replace with your desired app name
  web {
    redirect_uris = ["http://localhost/"]  # Replace with actual redirect URIs
  }
}

# Create a Service Principal associated with the Azure AD Application
resource "azuread_service_principal" "scrutiny_app_101_sp" {
  client_id = azuread_application.scrutiny_app_101.client_id
  
}

# Output the Application ID and Service Principal ID
output "application_id" {
  value = azuread_application.scrutiny_app_101.client_id
}

output "service_principal_id" {
  value = azuread_service_principal.scrutiny_app_101_sp.id
}


# Create a custom role definition
resource "azurerm_role_definition" "scrutiny_custom_role" {
  name        = "Scrutiny Terraform Executor"
  scope       = azurerm_resource_group.scrutiny_rg_101.id
  description = "Custom role for executing Terraform"
permissions {
  actions = [
    "Microsoft.Compute/virtualMachines/*",
    "Microsoft.Network/virtualNetworks/*",
    "Microsoft.Network/networkSecurityGroups/*",
    "Microsoft.Network/publicIPAddresses/*",
    "Microsoft.Network/loadBalancers/*",
    "Microsoft.Network/networkInterfaces/*",
    "Microsoft.KeyVault/vaults/*",
    "Microsoft.Compute/disks/read",
    "Microsoft.Compute/disks/delete",
    "Microsoft.Compute/disks/write",
    "Microsoft.Authorization/roleAssignments/read",
    "Microsoft.Storage/storageAccounts/read",
    "Microsoft.Storage/storageAccounts/write",
    "Microsoft.Resources/subscriptions/resourcegroups/read",
    "Microsoft.Resources/subscriptions/resourcegroups/write",
    "Microsoft.Resources/subscriptions/resourcegroups/*"  
  ]

  not_actions = []
}

  assignable_scopes = [
    azurerm_resource_group.scrutiny_rg_101.id,
  ]
}

resource "azurerm_role_definition" "scrutiny_storage_custom_role" {
  name        = "Scrutiny Storage Terraform Executor"
  scope       = azurerm_resource_group.scrutiny_storage_rg.id
  description = "Custom role for executing Terraform"
permissions {
  actions = [
    "Microsoft.Compute/virtualMachines/*",
    "Microsoft.Network/virtualNetworks/*",
    "Microsoft.Network/networkSecurityGroups/*",
    "Microsoft.Network/publicIPAddresses/*",
    "Microsoft.Network/loadBalancers/*",
    "Microsoft.Network/networkInterfaces/*",
    "Microsoft.KeyVault/vaults/*",
    "Microsoft.Compute/disks/read",
    "Microsoft.Compute/disks/delete",
    "Microsoft.Compute/disks/write",
    "Microsoft.Authorization/roleAssignments/read",
    "Microsoft.Storage/storageAccounts/read",
    "Microsoft.Storage/storageAccounts/write",
    "Microsoft.Resources/subscriptions/resourcegroups/read",
    "Microsoft.Resources/subscriptions/resourcegroups/write",
    "Microsoft.Resources/subscriptions/resourcegroups/*", 
    "Microsoft.Storage/storageAccounts/blobServices/*",
    "Microsoft.Storage/storageAccounts/listKeys/action",
    "Microsoft.Storage/storageAccounts/fileServices/*",
    "Microsoft.Storage/storageAccounts/queueServices/*",
    "Microsoft.Storage/storageAccounts/tableServices/*",
    "Microsoft.Storage/storageAccounts/delete",
    "Microsoft.Storage/storageAccounts/*",
  ]

  not_actions = []
}

  assignable_scopes = [
    azurerm_resource_group.scrutiny_storage_rg.id,
  ]
}


# Generate a random password
resource "random_password" "scrutiny_password" {
  length  = 17
  special = true
}


resource "azuread_service_principal_password" "sp_password" {
  service_principal_id = azuread_service_principal.scrutiny_app_101_sp.id
  end_date_relative    = "1000h" # 41 days
}

# Assign the custom role to the service principal
resource "azurerm_role_assignment" "scrutiny_role_assignment" {
  scope              = azurerm_resource_group.scrutiny_rg_101.id
  role_definition_id = azurerm_role_definition.scrutiny_custom_role.role_definition_resource_id
  principal_id       = azuread_service_principal.scrutiny_app_101_sp.id
}

resource "azurerm_role_assignment" "scrutiny_storage_role_assignment" {
  scope              = azurerm_resource_group.scrutiny_storage_rg.id
  role_definition_id = azurerm_role_definition.scrutiny_storage_custom_role.role_definition_resource_id
  principal_id       = azuread_service_principal.scrutiny_app_101_sp.id
}

# Output the service principal credentials
output "client_id" {
  value     = azuread_application.scrutiny_app_101.client_id
  sensitive = false
}

output "service_principal_secret" {
  value = azuread_service_principal_password.sp_password.value  
  sensitive = true
  
}

output "storage_rg_name" {
  value = azurerm_resource_group.scrutiny_storage_rg.name
  sensitive = false
}

output "storage_rg_id" {
  value = azurerm_resource_group.scrutiny_storage_rg.id
  sensitive = false
}
output "resource_group_name" {
  value = azurerm_resource_group.scrutiny_rg_101.name
  sensitive = false 
}
output "resource_group_id" {
  value = azurerm_resource_group.scrutiny_rg_101.id
  sensitive = false
}




