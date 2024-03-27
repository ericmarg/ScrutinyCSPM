package play

default volume_compliance = true

# Function to flatten the list of volumes from all instances
get_volumes(input_data) = [volume |
	instance := input_data.vms[_] # Iterate over each instance in the input
	volume := instance.volumes[_] # Iterate over each volume of the instance
]

# Check if any volume is not encrypted
volume_compliance = false {
	volume := get_volumes(input)[_] # Iterate over each volume in the flattened list
	not volume.encrypted # This evaluates to true if a volume is not encrypted
}

# Collect the IDs of volumes that are not encrypted
non_encrypted_volumes = {volume_id |
	volume := get_volumes(input)[_] # Iterate over each volume in the flattened list
	not volume.encrypted # Check if the volume is not encrypted
	volume_id := volume.id # Collect the Volume ID
}