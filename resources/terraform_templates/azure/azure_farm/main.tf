provider "azurerm" {
  features {}
}


module "keyvault" {
  source = "./modules/keyvault"

  # Pass other required variables to the keyvault module
    resource_group_name = var.resource_group_name
    rg_location = var.rg_location
    key_vault_name = var.key_vault_name
    validity_period_hours = var.validity_period_hours

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

