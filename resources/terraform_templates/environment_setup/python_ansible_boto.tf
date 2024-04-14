# Specify the required providers
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 2.13.0"
    }
  }
}

# Configure the Docker provider
provider "docker" {}

# Define variables for AWS access key and secret key
variable "aws_access_key" {
  description = "AWS access key"
  type        = string
  sensitive   = true
}

variable "aws_secret_key" {
  description = "AWS secret key"
  type        = string
  sensitive   = true
}

# Define the Docker image
resource "docker_image" "python_ansible_boto3" {
  name = "python-ansible-boto3"
  build {
    path = "."
    dockerfile = "Dockerfile"
    build_args = {
      AWS_ACCESS_KEY = var.aws_access_key
      AWS_SECRET_KEY = var.aws_secret_key
    }
  }
}

# Create a Dockerfile
resource "local_file" "dockerfile" {
  filename = "Dockerfile"
  content  = <<-EOF
  FROM python:3.9-slim

  # Install Ansible and boto3
  RUN apt-get update && \
      apt-get install -y sudo && \
      apt-get install -y sshpass && \
      apt-get clean && \
      rm -rf /var/lib/apt/lists/* && \
      pip install ansible boto3

  # Set environment variables for AWS access key and secret key
  ARG AWS_ACCESS_KEY
  ARG AWS_SECRET_KEY
  ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY
  ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_KEY

  # Set the entrypoint
  ENTRYPOINT ["ansible-playbook"]
  EOF
}