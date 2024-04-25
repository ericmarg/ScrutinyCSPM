provider "azurerm" {
  features {}
}


module "storage" {
  source = "./modules/storage"

  # Pass other required variables to the storage module
    rg_location = var.rg_location
    resource_group_name_storage = var.resource_group_name_storage

}

module "vnet" {
    source = "./modules/vnet"
    rg_location =            var.rg_location
    client_id = var.client_id
    client_secret = var.client_secret
    subscription_id = var.subscription_id
    tenant_id = var.tenant_id
    resource_group_name = var.resource_group_name
}
