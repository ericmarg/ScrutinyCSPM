package obj_storage

import rego.v1

default obj_storage_container_compliant := false
default aws_s3_mfa_enabled := false

obj_storage_container_compliant if {
    input.all_public_access_blocked = true
    input.versioning_enabled = true
}

aws_s3_mfa_enabled if {
    input.provider = "AWS"
    input.provider_specific.MFADeleteEnabled = true
}