
variable "rg_location" {
  description = "The Azure region where the Key Vault will be created"
  type        = string
  default     = "eastus"
}

variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
  default = "scrutiny_storage_rg_101"
}

variable "resource_group_name_id" {
  description = "The name of the resource group"
  type        = string
  
}

variable "resource_group_name_storage" {
  description = "The name of the resource group"
  type        = string
  
}

variable "resource_group_name_storage_id" {
  description = "The name of the resource group"
  type        = string
  
}

variable "key_vault_name" {
  description = "The name of the Azure Key Vault"
  type        = string
}

variable "subucription_id" {
  description = "The Azure subscription ID"
  type        = string
}

variable "tenant_id" {
  description = "The Azure tenant ID"
  type        = string
  
}