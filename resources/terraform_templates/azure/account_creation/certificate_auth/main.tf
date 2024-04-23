# Configure the Azure provider
provider "azurerm" {
  features {}
}

terraform {
  required_providers {
    azuread = {
      source  = "hashicorp/azuread"
    }
    tls = {
      source  = "hashicorp/tls"
    }
  }
}

resource "tls_private_key" "scrutiny_azure_tls_cert" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "tls_self_signed_cert" "azure" {
  private_key_pem = tls_private_key.scrutiny_azure_tls_cert.private_key_pem

  subject {
    common_name  = "Scrutiny Azure App Certificate 101"
  }

  allowed_uses = ["digital_signature"]

  # 5 years
  validity_period_hours = 24 * 365 * 5
  # Renew every year
  early_renewal_hours = 24 * 365 * 4
}

# Save the private key to a file
resource "local_file" "private_key" {
  filename = "test_certificate/private_key.pem"
  content  = tls_private_key.scrutiny_azure_tls_cert.private_key_pem
}

# Save the self-signed certificate to a file
resource "local_file" "self_signed_cert" {
  filename = "test_certificate/self_signed_cert.pem"
  content  = tls_self_signed_cert.azure.cert_pem
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


resource "azuread_service_principal_certificate" "scrutiny_app_101_cert_spX509" {
  service_principal_id = azuread_service_principal.scrutiny_app_101_certificate_sp.id
  type                 = "AsymmetricX509Cert"
  value                = tls_self_signed_cert.azure.cert_pem
  end_date = formatdate("YYYY-MM-DD'T'hh:mm:ssZ", tls_self_signed_cert.azure.validity_end_time)
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

resource "azurerm_key_vault" "scrutiny_key_vault_101" {
  sku_name = "standard"
  name                        = "scrutiny-key-vault-101"
  location                    = var.rg_location
  resource_group_name         = var.resource_group_name
  enabled_for_deployment      = true
  enabled_for_disk_encryption = true
  tenant_id                   = var.tenant_id
}

resource "azurerm_key_vault_access_policy" "scruntiny_key_vault_access_policy_101" {
  key_vault_id = azurerm_key_vault.scrutiny_key_vault_101.id

  tenant_id = var.tenant_id
  object_id = azuread_service_principal.scrutiny_app_101_certificate_sp.id

  certificate_permissions = [
    "Get",
    "List",
  ]

  key_permissions = [
    "Get",
    "List",
  ]

  secret_permissions = [
    "Get",
    "List",
  ]
}
# Output the service principal credentials
output "client_id" {
  value     = azuread_application.scrutiny_app_certificate_101.client_id
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




