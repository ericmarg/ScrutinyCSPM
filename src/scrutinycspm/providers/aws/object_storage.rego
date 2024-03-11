package obj_storage

import rego.v1

default obj_storage_container_compliant := false

obj_storage_container_compliant if {
    input.AllPublicAccessBlocked = true
    input.VersioningEnabled= true
}