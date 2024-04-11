variable "key_vault_name" {
  description = "The name of the Azure Key Vault"
  type        = string
  default     = "example-keyvault-01"
}

variable "location" {
  description = "The Azure region where the Key Vault will be created"
  type        = string
  default     = "eastus"
}

variable "resource_group_name" {
  description = "The name of the resource group where the Key Vault will be created"
  type        = string
  default     = "example-resource-group"
}