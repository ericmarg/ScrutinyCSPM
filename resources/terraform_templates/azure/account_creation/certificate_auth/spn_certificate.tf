# Configure the Azure provider
provider "azurerm" {
  features {}
}


variable "rg_location" {
  description = "The Azure region where the Key Vault will be created"
  type        = string
  default     = "eastus"
}

variable "resource_group_name_storage" {
  description = "The name of the resource group"
  type        = string
  default = "scrutiny_storage_rg_101"
}

variable "resource_group_name_storage_id" {
  description = "The name of the resource group"
  type        = string
  
}

variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
  default = "scrutiny_rg_101"
}

variable "resource_group_name_id" {
  description = "The name of the resource group"
  type        = string
  
}


# Create an Azure AD Application
resource "azuread_application" "scrutiny_app_certificate_101" {
  display_name = "Scrutiny Azure App Certificate 101"  # Replace with your desired app name
  web {
    redirect_uris = ["http://localhost/"]  # Replace with actual redirect URIs
  }
}

# Create a Service Principal associated with the Azure AD Application
resource "azuread_service_principal" "scrutiny_app_101_certificate_sp" {
  client_id = azuread_application.scrutiny_app_certificate_101.client_id
}

resource "azuread_service_principal_certificate" "sp_certficate_101" {
  service_principal_id = azuread_service_principal.scrutiny_app_101_certificate_sp.id
  type                 = "AsymmetricX509Cert"
  value                = file("test_certificate/cert.pem")
  end_date             = "2024-09-01T01:02:03Z"
}

# Output the Application ID and Service Principal ID
output "application_id" {
  value = azuread_application.scrutiny_app_certificate_101.client_id
}

output "service_principal_id" {
  value = azuread_service_principal.scrutiny_app_101_certificate_sp.id
}


# Create a custom role definition
resource "azurerm_role_definition" "scrutiny_custom_role_certificate" {
  name        = "Scrutiny Terraform Certificate Executor"
  scope       = var.resource_group_name_id
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
    var.resource_group_name_id,
  ]
}

resource "azurerm_role_definition" "scrutiny_storage_certificate_custom_role" {
  name        = "Scrutiny Storage Certificate Terraform Executor"
  scope       = var.resource_group_name_storage_id
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
    var.resource_group_name_storage_id,
  ]
}


# Assign the custom role to the service principal
resource "azurerm_role_assignment" "scrutiny_role_assignment" {
  scope              = var.resource_group_name_id
  role_definition_id = azurerm_role_definition.scrutiny_custom_role_certificate.role_definition_resource_id
  principal_id       = azuread_service_principal.scrutiny_app_101_certificate_sp.id
}

resource "azurerm_role_assignment" "scrutiny_storage_role_assignment" {
  scope              = var.resource_group_name_storage_id
  role_definition_id = azurerm_role_definition.scrutiny_storage_certificate_custom_role.role_definition_resource_id
  principal_id       = azuread_service_principal.scrutiny_app_101_certificate_sp.id
}

# Output the service principal credentials
output "client_id" {
  value     = azuread_application.scrutiny_app_certificate_101.application_id 
  sensitive = false
}

output "storage_rg_name" {
  value = var.resource_group_name_storage
  sensitive = false
}

output "storage_rg_id" {
  value = var.resource_group_name_id
  sensitive = false
}
output "resource_group_name" {
  value = var.resource_group_name
  sensitive = false 
}
output "resource_group_id" {
  value = var.resource_group_name_id
  sensitive = false
}




