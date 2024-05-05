import json
import jmespath

def transformation(json_content):
    # Parse the JSON content
    data = json.loads(json_content)

    # Define the JMESPath expression
    expression = '''
    buckets[*].{
        provider: 'aws',
        bucket_name: name,
        versioning_enabled: bucket_versioning.enabled || `false`,
        all_public_access_blocked: public_access_block.PublicAccessBlockConfiguration.BlockPublicAcls || `false` &&
                                   public_access_block.PublicAccessBlockConfiguration.BlockPublicPolicy || `false` &&
                                   public_access_block.PublicAccessBlockConfiguration.IgnorePublicAcls || `false` &&
                                   public_access_block.PublicAccessBlockConfiguration.RestrictPublicBuckets || `false`,
        provider_specific: {
            MFADeleteEnabled: mfa_delete.enabled || `false`
        }
    }
    '''

    # Search the JSON content using the JMESPath expression
    result = jmespath.search(expression, data)

    # Convert the result to JSON string
    json_output = json.dumps(result, indent=2)

    return json_output