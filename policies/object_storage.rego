package obj_storage

import rego.v1

# METADATA
# title: Enforce Object Storage Container Versioning
# description: Object storage containers must have versioning enabled.
# custom:
#   remediation_guidance:
#     enable_public_access_block:
#        aws: For S3 buckets, call the PutPublicAccessBlock API [1][2]
#        azure: TBC
#     enable_versioning:
#        aws: For S3 buckets, call the PutBucketVersioning API [1][2] with Status of `Enabled`.
#        azure: TBC
enforce_versioning_enabled := non_compliant_decision if {
    input.versioning_enabled = false
    
	annotation := rego.metadata.rule()

	non_compliant_decision := 
    {
     "message": annotation.description,
     "remediation_guidance": annotation.custom.remediation_guidance.enable_versioning.aws,
    }
}

# METADATA
# title: Enforce Public Access Block
# description: Object storage containers must have all public access options disabled.
# custom:
#   remediation_guidance:
#     enable_public_access_block:
#        aws: For S3 buckets, call the PutPublicAccessBlock API [1][2]
#        azure: TBC
enforce_public_access_block := non_compliant_decision if {
    input.all_public_access_blocked = false
    
	annotation := rego.metadata.rule()

	non_compliant_decision := 
    {
     "message": annotation.description,
     "remediation_guidance": annotation.custom.remediation_guidance.enable_public_access_block.aws,
    }
}

# METADATA
# title: Enforce MFA Delete on S3 Buckets (AWS S3 specific rule)
# description: S3 Buckets must have MFA delete enabled
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