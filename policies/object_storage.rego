package obj_storage

import rego.v1

# METADATA
# title: Enforce Public Access Block and Versioning
# description: > Object storage containers must have public internet access blocked and versioning enabled. 
#                Versioning prevents the chance of an object being permanently deleted by accident.
#                Enabling Public Access Block configuration lowers the risk of accidental disclosure of sensitive data.
# custom:
#   remediation_guidance:
#     enable_public_access_block:
#        aws: > For S3 buckets, call the PutPublicAccessBlock API [1][2] , and set the following configuration parameters to `true`: 
#         
#               "BlockPublicAcls"
#               "IgnorePublicAcls" 
#               "BlockPublicPolicy"
#               "RestrictPublicBuckets"       
#
#               NOTE: If you are managing resources with Infrastructure as Code software,  
#                     please refer to your provider's documentation on how to safely remediate your resources to avoid configuration drift.
#
#               For more information on blocking access to your S3 buckets, 
#               please see the S3 Documentation page "Blocking public access to your Amazon S3 storage" [3].
#
#               [1] https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutPublicAccessBlock.html
#               [2] https://docs.aws.amazon.com/cli/latest/reference/s3api/put-public-access-block.html
#               [3] https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html
#        azure: TBC
#     enable_versioning:
#        aws: > For S3 buckets, call the PutBucketVersioning API [1][2] with a VersioningConfiguration [3] that has a Status of `Enabled`.
#
#               NOTE: If you are managing resources with Infrastructure as Code software,  
#                     please refer to your provider's documentation on how to safely remediate your resources to avoid configuration drift.
#
#               For more information about S3 Bucket Versioning, please see the S3 Documentation [4].
#
#               [1] https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketVersioning.html
#               [2] https://docs.aws.amazon.com/cli/latest/reference/s3api/put-bucket-versioning.html
#               [3] https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketVersioning.html#API_PutBucketVersioning_RequestSyntax
#               [4] https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html
#        azure: TBC
enforce_versioning_block_public_access := non_compliant_decision if {
    versioning_or_block_public_access_not_compliant(input)

    annotation := rego.metadata.rule()

    if input.all_public_access_blocked == false {
        public_access_block_remediation := [annotation.custom.remediation_guidance.enable_public_access_block.aws]
    } else {
        public_access_block_remediation := []
    }

    if input.versioning_enabled == false {
        versioning_remediation := [annotation.custom.remediation_guidance.enable_versioning.aws]
    } else {
        versioning_remediation := []
    }

    non_compliant_decision := {
        "message": annotation.description
        "remediation_guidance": array.concat(public_access_block_remediation, versioning_remediation )
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
# description: > S3 Buckets must have MFA delete enabled, 
#                which makes it that only the AWS Account root user with MFA device 
#                can permanently delete object versions or otherwise change S3 Bucket Versioning Configuration. 
#                
#                This configuration adds more friction to the object deletion process, which reduces the risk of accidental object deletion.
# custom:
#   remediation_guidance: 
#     enable_mfa_delete:
#       aws: > MFA Delete can only be activated through the CLI or AWS SDK using the AWS account root user. 
#              The AWS account root user must have an MFA device configured before activating MFA Delete on any S3 bucket.
#              For a detailed guide on how to activate MFA delete for your S3 buckets, please see the relevant AWS documentation [1][2].
#                           
#              [1] https://repost.aws/knowledge-center/s3-bucket-mfa-delete
#              [2] https://docs.aws.amazon.com/AmazonS3/latest/userguide/MultiFactorAuthenticationDelete.html
enforce_aws_s3_mfa_enabled := non_compliant_decision if {
    input.provider = "AWS"
    input.provider_specific.MFADeleteEnabled = false

    annotation := rego.metadata.rule()
    non_compliant_decision := {
        "message": annotation.description
        "remediation_guidance": annotation.custom.remediation_guidance.enable_mfa_delete.aws
    }
}