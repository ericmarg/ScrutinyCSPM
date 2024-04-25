package azure.nsg

default allow = false

# Policy to check if SSH access is allowed from any source
deny[msg] {
    input.securityRules[_].access == "Allow"
    input.securityRules[_].direction == "Inbound"
    input.securityRules[_].protocol == "TCP"
    input.securityRules[_].sourceAddressPrefix == "*"
    input.securityRules[_].sourcePortRange == "*"
    input.securityRules[_].destinationPortRange == "22"
    msg := "SSH access is allowed from any source"
}

# Policy to check if RDP access is allowed from any source
deny[msg] {
    input.securityRules[_].access == "Allow"
    input.securityRules[_].direction == "Inbound"
    input.securityRules[_].protocol == "TCP"
    input.securityRules[_].sourceAddressPrefix == "*"
    input.securityRules[_].sourcePortRange == "*"
    input.securityRules[_].destinationPortRange == "3389"
    msg := "RDP access is allowed from any source"
}

# Policy to check if any inbound rule allows access from any source
deny[msg] {
    input.securityRules[_].access == "Allow"
    input.securityRules[_].direction == "Inbound"
    input.securityRules[_].sourceAddressPrefix == "*"
    msg := "Inbound rule allows access from any source"
}

allow {
    count(deny) == 0
}