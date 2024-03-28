package play

default sg_compliance = true

# Function to flatten the list of security groups from all VMs
get_security_groups(input_data) = [sg |
    vm := input_data.vms[_] # Iterate over each VM in the input
    sg := vm.security_groups[_] # Iterate over each security group of the VM
]

# Check if any security group allows public access
sg_compliance = false {
    sg := get_security_groups(input)[_] # Iterate over each security group in the flattened list
    rule := sg.rules[_] # Iterate over each rule in the security group
    rule.IpRanges[_] == "0.0.0.0/0" # Check if any rule allows access from any IP (public access)
}

# Collect the IDs of security groups that allow public access
sgs_with_public_access = {sg_id |
    sg := get_security_groups(input)[_] # Iterate over each security group in the flattened list
    rule := sg.rules[_] # Iterate over each rule in the security group
    rule.IpRanges[_] == "0.0.0.0/0" # Check if any rule allows access from any IP (public access)
    sg_id := sg.id # Collect the security group ID
}
