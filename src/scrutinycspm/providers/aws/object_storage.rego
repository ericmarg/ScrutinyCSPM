package object_storage

import rego.v1

default storage_container_compliance := false

storage_container_compliant if {
    input.AllPublicAccessBlocked = true
    input.Encrypted = true
}