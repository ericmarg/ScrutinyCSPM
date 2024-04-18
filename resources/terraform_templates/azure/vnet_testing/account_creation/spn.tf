# Provider configuration
provider "azurerm" {
  features {}
}

# Create a resource group
resource "azurerm_resource_group" "rg" {
  name     = "terraform-rg"
  location = "East US"
}

# Create an Azure AD application
resource "azuread_application" "scrutiny-app-07" {
  display_name = "Terraform Service Principal"
}

# Create an Azure AD service principal
resource "azuread_service_principal" "sp" {
  client_id = azuread_application.scrutiny-app-07.application_id
}

# Create a custom role definition
resource "azurerm_role_definition" "custom_role" {
  name        = "Terraform Executor"
  scope       = azurerm_resource_group.rg.id
  description = "Custom role for executing Terraform"

  permissions {
    actions = [
      "Microsoft.Compute/virtualMachines/*",
      "Microsoft.Network/virtualNetworks/*",
      "Microsoft.Network/networkSecurityGroups/*",
      "Microsoft.Network/publicIPAddresses/*",
      "Microsoft.Network/loadBalancers/*",
      "Microsoft.Network/networkInterfaces/*",
    ]
    not_actions = []
  }

  assignable_scopes = [
    azurerm_resource_group.rg.id,
  ]
}

# Assign the custom role to the service principal
resource "azurerm_role_assignment" "role_assignment" {
  scope              = azurerm_resource_group.rg.id
  role_definition_id = azurerm_role_definition.custom_role.role_definition_resource_id
  principal_id       = azuread_service_principal.sp.object_id
}

# Generate a random password
resource "random_password" "password" {
  length  = 16
  special = true
}

# Set the password for the service principal
resource "azuread_service_principal_password" "sp_password" {
  service_principal_id = azuread_service_principal.sp.object_id
  value                = random_password.password.result
  end_date_relative    = "500h" # 20 days
}

# Output the service principal credentials
output "client_id" {
  value     = azuread_application.app.application_id
  sensitive = true
}

output "client_secret" {
  value     = azuread_service_principal_password.sp_password.value
  sensitive = true
}