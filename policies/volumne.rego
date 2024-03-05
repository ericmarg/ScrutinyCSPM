package play

default volume_compliance = true

# Helper rule to flatten the list of volumes from all instances
all_volumes = [volume |
	instance := input[_] # Iterate over each instance in the input
	volume := instance.Volumes[_] # Iterate over each volume of the instance
]

# Check if any volume is not encrypted
volume_compliance = false {
	volume := all_volumes[_] # Iterate over each volume in all_volumes
	not volume.Encrypted # This evaluates to true if a volume is not encrypted
}

# Collect the IDs of volumes that are not encrypted
non_encrypted_volumes = {volume_id |
	instance := input[_] # Iterate over each instance in the input
	volume := instance.Volumes[_] # Iterate over each volume of the instance
	not volume.Encrypted # Check if the volume is not encrypted
	volume_id := volume.VolumeId # Collect the Volume ID
}
