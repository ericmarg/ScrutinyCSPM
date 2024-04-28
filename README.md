

# ScrutinyCSPM
ScrutinyCSPM is an open-source Cloud Security Posture Management (CSPM) offering from a team of Harvard Extension School graduate students. 
It provides resource scanning and remediation based on Rego policy rules. ScrutinyCSPM uses the Open Policy Agent (OPA) to evaluate policy decisions.

[Documents (docs/markdown)](docs/markdown/)

## Prerequisites

- Docker installed on your system ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed on your system ([Install Docker Compose](https://docs.docker.com/compose/install/))

## How to Run

1. Open a terminal and enter this command to clone this repository to your local machine:

   ```bash
   git clone https://github.com/ericmarg/ScrutinyCSPM.git
   ```

2. Navigate to the cloned repository and copy the Dockerfile to it:

   ```bash
   cd ScrutinyCSPM
   ```

3. Run the Docker container and it's dependencies:

   ```bash
   docker compose up -d
   ```
4. Add credentials to the running container. 

   Currently the Scrutiny CSPM application requires the deployment of AWS and Azure credentials.  These steps are documented in the following document prior to step 5

   [General Configuration](General_Configuration.MD)

   [Azure Environment Vars for Cloud Authentication](docs/markdown/azure_environment_vars.md)

   [AWS Credentials File]()


4. You can now access the ScrutinyCSPM program by entering the following command:

   ```bash
   docker exec -it scrutiny-cspm /bin/bash -c "python /scrutinycspm/cli/main.py"
   ```

5. You can now enter commands to interact with the program.
   
   Example:
   
   ```bash
   Enter a command (or 'quit' to exit): help
   ```

6. To exit the program, type `quit` at the prompt.

## Commands
Provided the Terraform Files found in the in Terraform folders [Terrform Test Azure Farm](resources/terraform_templates/azure/azure_farm/) and [Terraform Test AWS Farm](resources/terraform_templates/aws/vpc/) have been executed, then the following commands can be tested:

```bash

azure nsg
azure vm
azure vnet
azure storage

aws summary us-east-2
aws ec2 us-east-2
aws s3 us-east-2
aws security-group us-east-2

```

## Notes
- ScrutinyCSPM ships with a set of security policies and Terraform plans to help with testing.
- Download and customize policies to align remediation suggestions with your organization's security posture goals.

## License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), 
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
