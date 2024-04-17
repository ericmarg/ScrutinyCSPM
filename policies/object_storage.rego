package obj_storage

import rego.v1

# METADATA
# title: Enforce Object Storage Container Versioning
# description: Object storage containers must have versioning enabled.
# custom:
#   remediation_guidance:
#     enable_versioning:
#        aws: obj_storage/aws/enable_versioning.txt
#        azure: TBC
enforce_versioning_enabled := non_compliant_decision if {
	input.versioning_enabled = false

	annotation := rego.metadata.rule()

	remediation_guidance := annotation.custom.remediation_guidance.enable_versioning.aws
	non_compliant_decision := {
		"rule_description": annotation.description,
		"status": "Not Compliant",
		"remediation_guidance": remediation_guidance,
	}
}

# METADATA
# title: Enforce Object Storage Container Versioning
# description: Object storage containers must have versioning enabled.
# custom:
#   remediation_guidance:
#     enable_versioning:
#        aws: obj_storage/aws/enable_versioning.txt
#        azure: TBC
enforce_versioning_enabled := compliant_decision if {
	input.versioning_enabled = true

	annotation := rego.metadata.rule()

	compliant_decision := {
		"rule_description": annotation.description,
		"status": "Compliant",
	}
}

# METADATA
# title: Enforce Public Access Block
# description: Object storage containers must have all public access options disabled.
# custom:
#   remediation_guidance:
#     enable_public_access_block:
#        aws: obj_storage/aws/enable_public_access_block.txt
#        azure: TBC
enforce_public_access_block := non_compliant_decision if {
	input.all_public_access_blocked = false

	annotation := rego.metadata.rule()

	remediation_guidance := annotation.custom.remediation_guidance.enable_public_access_block.aws

	non_compliant_decision := {
		"rule_description": annotation.description,
		"status": "Not Compliant",
		"remediation_guidance": remediation_guidance,
	}
}

# METADATA
# title: Enforce Public Access Block
# description: Object storage containers must have all public access options disabled.
# custom:
#   remediation_guidance:
#     enable_public_access_block:
#        aws: obj_storage/aws/enable_public_access_block.txt
#        azure: TBC
enforce_public_access_block := compliant_decision if {
	input.all_public_access_blocked = true

	annotation := rego.metadata.rule()
	compliant_decision := {
		"rule_description": annotation.description,
		"status": "Compliant",
	}
}

# METADATA
# title: Enforce MFA Delete on S3 Buckets (AWS S3 specific rule)
# description: S3 Buckets must have MFA delete enabled
# custom:
#  remediation_guidance:
#   enable_mfa_delete:
#    aws: obj_storage/aws/enable_mfa_delete.txt
enforce_aws_s3_mfa_enabled := non_compliant_decision if {
	input.provider = "AWS"
	input.provider_specific.MFADeleteEnabled = false

	annotation := rego.metadata.rule()
	non_compliant_decision := {
		"rule_description": annotation.description,
		"status": "Not Compliant",
		"remediation_guidance": annotation.custom.remediation_guidance.enable_mfa_delete.aws,
	}
}

# METADATA
# title: Enforce MFA Delete on S3 Buckets (AWS S3 specific rule)
# description: S3 Buckets must have MFA delete enabled
# custom:
#  remediation_guidance:
#   enable_mfa_delete:
#    aws: obj_storage/aws/enable_mfa_delete.txt
enforce_aws_s3_mfa_enabled := compliant_decision if {
	input.provider = "AWS"
	input.provider_specific.MFADeleteEnabled = true

	annotation := rego.metadata.rule()
	compliant_decision := {
		"rule_description": annotation.description,
		"status": "Compliant",
	}
}
