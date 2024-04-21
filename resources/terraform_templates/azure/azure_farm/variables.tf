variable "key_vault_name" {
  description = "The name of the Azure Key Vault"
  type        = string
  default     = "scrutiny-keyvault-01"
}

variable "rg_location" {
  description = "The Azure region where the Key Vault will be created"
  type        = string
  default     = "eastus"
}


variable "validity_period_hours" {
  description = "The validity period of the certificate in hours"
  type        = string
  # 1000 hours = 41 days
  default     = "1000"
} 


variable "resource_group_name" {
  description = "The name of the resource group where the resources will be created"
  type        = string
  default     = "scrutiny_rg_101"
}

variable "client_id" {
  description = "The client ID for the Azure service principal."
}

variable "client_secret" {
  description = "The client secret for the Azure service principal."
}

variable "tenant_id" {
  description = "Azure tenant ID"
}

variable "subscription_id" {
  description = "Azure subscription ID"
}