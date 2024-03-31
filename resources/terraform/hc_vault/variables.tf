
variable "vault_address" {
  description = "HashiCorp Vault server address"
  type        = string
  sensitive = true
  default     = "https://vault.example.com:8200"
  
}

variable "certificate_path" {
  description = "Path to cerfiticate to upload to HashiCorp Vault"
  type        = string
  sensitive = true
  default     = "/home/robert/tmp1_xf3jfr.pem"
}