provider "vault" {
  address = var.vault_address  # Replace with your Vault server address
}

resource "vault_mount" "azure_certificates" {
  path        = "azure/certificates"
  type        = "kv"
  description = "Mount for Azure service principal certificates"
}

resource "vault_generic_secret" "azure_certificate" {
  path      = "${vault_mount.azure_certificates.path}/test_scrutinycspm"
  data_json = jsonencode(
    {
      certificate = file(var.certificate_path)
    }
  )
}

