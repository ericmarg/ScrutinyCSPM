# Provider configuration
provider "aws" {
  region = "us-east-2"  # Replace with your desired region
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
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-2a"  # Replace with your desired AZ
  tags = {
    Name = "web-subnet"
  }
}

# Application Server Subnet
resource "aws_subnet" "app" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-2b"  # Replace with your desired AZ
  tags = {
    Name = "app-subnet"
  }
}

# Database Subnet 1
resource "aws_subnet" "db_1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "us-east-2a"  # Replace with your desired AZ
  tags = {
    Name = "db-subnet-1"
  }
}

# Database Subnet 2
resource "aws_subnet" "db_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.4.0/24"
  availability_zone = "us-east-2b"  # Replace with your desired AZ
  tags = {
    Name = "db-subnet-2"
  }
}

# Database Subnet Group
resource "aws_db_subnet_group" "default" {
  name        = "aws_db_subnet_group"
  subnet_ids  = [aws_subnet.db_1.id, aws_subnet.db_2.id]
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
  ami           = "ami-0900fe555666598a2"  # Replace with your desired AMI ID
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
  ami           = "ami-0900fe555666598a2"  # Replace with your desired AMI ID
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.app.id
  vpc_security_group_ids = [aws_security_group.app.id]
  tags = {
    Name = "app-server-${count.index + 1}"
  }
}

# Database (RDS)
resource "aws_db_instance" "db" {
  engine                 = "mysql"
  instance_class         = "db.m6id.large"
  db_name                = "mydb"
  username               = "admin"
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.default.name
  vpc_security_group_ids = [aws_security_group.db.id]
  allocated_storage      = 20
  skip_final_snapshot    = true
}

# Variable for database password
variable "db_password" {
  description = "Enter the password for the database"
  type        = string
  sensitive   = true
}