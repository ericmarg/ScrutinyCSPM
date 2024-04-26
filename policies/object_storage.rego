package obj_storage

import rego.v1

# METADATA
# title: Enforce Object Storage Container Versioning (Non Compliant Decision)
# description: Object storage containers must have versioning enabled.
# custom:
#   remediation_guidance: obj_storage/enable_versioning.txt
enforce_versioning_enabled := non_compliant_decision if {
	input.versioning_enabled = false

	annotation := rego.metadata.rule()

	non_compliant_decision := {
		"provider": input.provider,
		"rule_description": annotation.description,
		"status": "Not Compliant",
		"remediation_guidance": annotation.custom.remediation_guidance,
	}
}

# METADATA
# title: Enforce Object Storage Container Versioning (Compliant Decision)
# description: Object storage containers must have versioning enabled.
enforce_versioning_enabled := compliant_decision if {
	input.versioning_enabled = true

	annotation := rego.metadata.rule()

	compliant_decision := {
		"provider": input.provider,
		"rule_description": annotation.description,
		"status": "Compliant",
	}
}

# METADATA
# title: Enforce Public Access Block (Not Compliant Decision)
# description: Object storage containers must have all public access options disabled.
# custom:
#   remediation_guidance: obj_storage/enable_public_access_block.txt
enforce_public_access_block := non_compliant_decision if {
	input.all_public_access_blocked = false

	annotation := rego.metadata.rule()

	non_compliant_decision := {
		"provider": input.provider,
		"rule_description": annotation.description,
		"status": "Not Compliant",
		"remediation_guidance": annotation.custom.remediation_guidance,
	}
}

# METADATA
# title: Enforce Public Access Block (Compliant Decision)
# description: Object storage containers must have all public access options disabled.
enforce_public_access_block := compliant_decision if {
	input.all_public_access_blocked = true

	annotation := rego.metadata.rule()
	compliant_decision := {
		"provider": input.provider,
		"rule_description": annotation.description,
		"status": "Compliant",
	}
}

# METADATA
# title: Enforce MFA Delete on S3 Buckets (Non Compliant Decision)
# description: S3 Buckets must have MFA delete enabled
# custom:
#  remediation_guidance: obj_storage/enable_mfa_delete.txt
enforce_aws_s3_mfa_enabled := non_compliant_decision if {
	input.provider = "aws"
	input.provider_specific.MFADeleteEnabled = false

	annotation := rego.metadata.rule()
	non_compliant_decision := {
		"provider": input.provider,
		"rule_description": annotation.description,
		"status": "Not Compliant",
		"remediation_guidance": annotation.custom.remediation_guidance,
	}
}

# METADATA
# title: Enforce MFA Delete on S3 Buckets (Compliant Decision)
# description: S3 Buckets must have MFA delete enabled
enforce_aws_s3_mfa_enabled := compliant_decision if {
	input.provider = "aws"
	input.provider_specific.MFADeleteEnabled = true

	annotation := rego.metadata.rule()
	compliant_decision := {
		"provider": input.provider,
		"rule_description": annotation.description,
		"status": "Compliant",
	}
}
