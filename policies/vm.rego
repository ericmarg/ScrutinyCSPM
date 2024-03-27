package play

default vm_compliance = true

# Function to flatten the list of VMs from the input data
get_vms(input_data) = [vm |
    vm := input_data.vms[_] # Iterate over each VM in the input
]

# Check if any VM has a public IP address
vm_compliance = false {
    vm := get_vms(input)[_] # Iterate over each VM in the flattened list
    vm.public_ip # This evaluates to true if a VM has a public IP address
}

# Collect the IDs of VMs that have public IP addresses
vms_with_public_ip = {vm_id |
    vm := get_vms(input)[_] # Iterate over each VM in the flattened list
    vm.public_ip # Check if the VM has a public IP address
    vm_id := vm.id # Collect the VM ID
}
