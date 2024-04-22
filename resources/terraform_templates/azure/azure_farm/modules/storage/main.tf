# Provider configuration
provider "azurerm" {
  features {}

}

variable "rg_location" {

  description = "The name of the resource location"
  type        = string
  default = "eastus"

}

variable "resource_group_name_storage" {
  description = "The name of the resource group"
  type        = string
  default = "scrutiny_storage_rg_101"
}

resource "azurerm_storage_account" "scrutiny_public_storage" {
name                = "scrpublicstorageaccount"
resource_group_name = var.resource_group_name_storage
location            = var.rg_location
account_tier        = "Standard"
account_replication_type = "LRS"
enable_https_traffic_only       = false
public_network_access_enabled   = true

}

resource "azurerm_storage_account" "scrutiny_private_storage" {
name                = "scrprivatestorageaccount"

resource_group_name = var.resource_group_name_storage
location            = var.rg_location
account_tier        = "Standard"
account_replication_type = "LRS"
enable_https_traffic_only       = true
public_network_access_enabled   = false
allow_nested_items_to_be_public = false

}

resource "azurerm_storage_account" "scrutiny_storage_with_versioning" {
name                = "scrstoragewithversioning"
resource_group_name = var.resource_group_name_storage
location            = var.rg_location
account_tier        = "Standard"
account_replication_type = "LRS"
enable_https_traffic_only       = true
blob_properties {
versioning_enabled = true
}
}

resource "azurerm_storage_account" "storage_without_versioning" {
name                = "scrstoragewoversioning"
resource_group_name = var.resource_group_name_storage
location            = var.rg_location
account_tier        = "Standard"
account_replication_type = "LRS"

blob_properties {
versioning_enabled = false
}
}