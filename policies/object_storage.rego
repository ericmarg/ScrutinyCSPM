package obj_storage

import rego.v1

# METADATA
# title: Enforce Public Access Block and Versioning
# description: Object storage containers must have public internet access blocked and versioning enabled.
# custom:
#   remediation_guidance:
#     enable_public_access_block:
#        aws: For S3 buckets, call the PutPublicAccessBlock API [1][2]
#        azure: TBC
#     enable_versioning:
#        aws: For S3 buckets, call the PutBucketVersioning API [1][2] with Status of `Enabled`.
#        azure: TBC
enforce_versioning_block_public_access := non_compliant_decision if {
	versioning_or_block_public_access_not_compliant(input)

	annotation := rego.metadata.rule()

	public_access_block_remediation := annotation.custom.remediation_guidance.enable_public_access_block.aws
	versioning_remediation := annotation.custom.remediation_guidance.enable_versioning.aws

	non_compliant_decision := 
    {
     "message": annotation.description,
     "remediation_guidance": concat(" ", [public_access_block_remediation, versioning_remediation])
    }
}

versioning_or_block_public_access_not_compliant(input_data) if {
	input_data.all_public_access_blocked = false
}

versioning_or_block_public_access_not_compliant(input_data) if {
	input_data.versioning_enabled = false
}

# METADATA
# title: Enforce MFA Delete on S3 Buckets (AWS S3 specific rule)
# description: S3 Buckets must have MFA delete enabled,\n
# custom:
#  remediation_guidance:
#   enable_mfa_delete:
#    aws: MFA Delete can only be activated through the CLI or AWS SDK using the AWS account root user.
enforce_aws_s3_mfa_enabled := non_compliant_decision if {
	input.provider = "AWS"
	input.provider_specific.MFADeleteEnabled = false

	annotation := rego.metadata.rule()
	non_compliant_decision := {
		"message": annotation.description,
		"remediation_guidance": annotation.custom.remediation_guidance.enable_mfa_delete.aws,
	}
}