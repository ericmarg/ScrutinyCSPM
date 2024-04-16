# Provider configuration
provider "aws" {
  region = "us-west-2"
}

# VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "my-vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id
}

# Web Server Subnet
resource "aws_subnet" "web" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
  tags = {
    Name = "web-subnet"
  }
}

# Application Server Subnet
resource "aws_subnet" "app" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.2.0/24"
  tags = {
    Name = "app-subnet"
  }
}

# Web Server Security Group
resource "aws_security_group" "web" {
  name_prefix = "web-sg-"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Application Server Security Group
resource "aws_security_group" "app" {
  name_prefix = "app-sg-"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
  }
}

# Database Security Group
resource "aws_security_group" "db" {
  name_prefix = "db-sg-"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }
}

# Web Server Instances
resource "aws_instance" "web" {
  count         = 2
  ami           = "ami-0c55b159cbfafe1f0"  # Replace with your desired AMI ID
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.web.id
  vpc_security_group_ids = [aws_security_group.web.id]
  tags = {
    Name = "web-server-${count.index + 1}"
  }
}

# Application Server Instances
resource "aws_instance" "app" {
  count         = 2
  ami           = "ami-0c55b159cbfafe1f0"  # Replace with your desired AMI ID
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.app.id
  vpc_security_group_ids = [aws_security_group.app.id]
  tags = {
    Name = "app-server-${count.index + 1}"
  }
}

# Database (RDS)
resource "aws_db_instance" "db" {
  engine         = "mysql"
  instance_class = "db.t2.micro"
  db_name        = "mydb"
  username       = "admin"
  password       = "password123"  # Replace with your desired password
  vpc_security_group_ids = [aws_security_group.db.id]
  skip_final_snapshot    = true
}