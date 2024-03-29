provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example_vault_rg" {
  name     = var.resource_group_name
  location = var.location
}

data "azurerm_client_config" "current" {}

resource "azurerm_role_assignment" "example_role_assignment" {
  scope                = azurerm_resource_group.example_vault_rg.id
  role_definition_name = "Reader"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_key_vault" "example_vault_01" {
  name                = var.key_vault_name
  location            = var.location
  resource_group_name = azurerm_resource_group.example_vault_rg.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"
}

resource "tls_private_key" "example_cert_key" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

resource "tls_self_signed_cert" "example_cert" {
  private_key_pem = tls_private_key.example_cert_key.private_key_pem

  subject {
    common_name  = "example-cert"
    organization = "Example Org"
  }

  validity_period_hours = 87600 # 10 years

  allowed_uses = [
    "key_encipherment",
    "digital_signature",
    "client_auth"
  ]
}

resource "azuread_application" "example_app" {
  display_name = "Example Service Principal"

  required_resource_access {
    resource_app_id = "00000003-0000-0000-c000-000000000000" # Microsoft Graph API
    resource_access {
      id   = "e1fe6dd8-ba31-4d61-89e7-88639da4683d" # User.Read.All
      type = "Scope"
    }
  }
}

resource "azuread_service_principal" "example_sp" {
client_id = azuread_application.example_app.client_id
}

resource "azuread_service_principal_certificate" "example_sp_cert" {
  service_principal_id = azuread_service_principal.example_sp.id
  type                 = "AsymmetricX509Cert"
  value                = tls_self_signed_cert.example_cert.cert_pem
}


resource "azurerm_key_vault_access_policy" "example_sp_access_policy" {
  key_vault_id = azurerm_key_vault.example_vault_01.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = azuread_service_principal.example_sp.object_id

  certificate_permissions = [
    "Get",
    "List",
    "Update",
    "Create",
    "Import",
    "Delete",
    "Recover",
    "Backup",
    "Restore",
    "ManageContacts",
    "ManageIssuers",
    "GetIssuers",
    "ListIssuers",
    "SetIssuers",
    "DeleteIssuers",
  ]
}