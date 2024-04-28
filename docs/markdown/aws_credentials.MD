# Creating an AWS Credential File for boto3

To use boto3 for accessing AWS services, you need to set up an AWS credential file that contains your AWS access key ID and secret access key. Follow the steps below for your operating system to create the credential file.

## Prerequisites

- AWS account
- AWS IAM user with programmatic access
- AWS access key ID and secret access key for the IAM user

## Windows

1. Open the Command Prompt or PowerShell.

2. Run the following command to create the `.aws` directory in your user directory:

```bash 
mkdir %USERPROFILE%.aws

```
3. Navigate to the `.aws` directory:

```bash
cd %USERPROFILE%.aws
```

4. Create a new file named `credentials` (without any file extension) using a text editor, such as Notepad:


### notepad credentials
5. In the file, add the following lines, replacing `YOUR_ACCESS_KEY_ID` and `YOUR_SECRET_ACCESS_KEY` with your actual AWS access key ID and secret access key:

[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY


6. Save the file and close the text editor. In nano, press `Ctrl + X`, then `Y`, and finally `Enter` to save and exit.

## Usage in boto3

Once you have created the AWS credential file, boto3 will automatically detect and use the credentials from the file when making requests to AWS services.

You can now use boto3 in your Python scripts without explicitly specifying the access key ID and secret access key.

```python
import boto3

# Create an S3 client
s3_client = boto3.client('s3')

# Use the S3 client to perform operations
# ...

# WARNING: 

Make sure to keep your AWS credentials secure and do not share them with others.