# Configure the AWS provider
provider "aws" {
  region = "us-east-2"  # Replace with your desired region
}


# Create a security group for the EC2 instances
resource "aws_security_group" "test_sg" {
  name_prefix = "test-sg-"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create three EC2 instances
resource "aws_instance" "test_instance" {
  count         = 3
  ami           = "ami-0900fe555666598a2"  # Replace with your desired AMI ID
  instance_type = "t2.micro"
  key_name      = "aws_ec2_key_testing"  # Replace with your key pair name

  vpc_security_group_ids = [aws_security_group.test_sg.id]

  tags = {
    Name = "test-instance-${count.index + 1}"
  }
}

# Output the public IP addresses of the instances
output "instance_public_ips" {
  value = aws_instance.test_instance[*].public_ip
}