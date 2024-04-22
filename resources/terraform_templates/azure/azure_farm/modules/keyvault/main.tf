provider "azurerm" {
  features {}
}

variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
}

variable "validity_period_hours" {
  description = "The validity period of the certificate in hours"
  type        = string
}

variable "rg_location" {
  description = "The name of the resource location"
  type        = string
}

variable "key_vault_name" {
  description = "The name of the Azure Key Vault"
  type      = string
}

variable "client_id" {
  description = "The ID of the service principal"
  type        = string
}

data "azurerm_client_config" "current" {}

resource "azurerm_role_assignment" "scrutiny_role_assignment" {
  scope                = azurerm_key_vault.scrutiny_vault_01.id
  role_definition_name = "Reader"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_key_vault" "scrutiny_vault_01" {
  name                = var.key_vault_name
  location            = var.rg_location
  resource_group_name = var.resource_group_name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"
}

resource "tls_private_key" "scrutiny_cert_key" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

resource "tls_self_signed_cert" "scrutiny_cert" {
  private_key_pem = tls_private_key.scrutiny_cert_key.private_key_pem

  subject {
    common_name  = "scrutiny-cert"
    organization = "Scrutiny CSPM"
  }

  validity_period_hours = var.validity_period_hours

  allowed_uses = [
    "key_encipherment",
    "digital_signature",
    "client_auth"
  ]
}

resource "azuread_service_principal" "scrutiny_example_sp" {
client_id = var.client_id
}

resource "azuread_service_principal_certificate" "scrutiny_example_sp_cert" {
  service_principal_id = azuread_service_principal.scrutiny_example_sp.id
  type                 = "AsymmetricX509Cert"
  value                = tls_self_signed_cert.scrutiny_cert.cert_pem
}


resource "azurerm_key_vault_access_policy" "example_sp_access_policy" {
  key_vault_id = azurerm_key_vault.scrutiny_vault_01.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = azuread_service_principal.scrutiny_example_sp.id

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