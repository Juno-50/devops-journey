variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}

variable "db_username" {
  description = "MySQL admin username"
  type        = string
  default     = "admin"
}

variable "db_password" {
  description = "MySQL admin password"
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "WordPress database name"
  type        = string
  default     = "wordpress"
}

variable "allowed_ssh_ip" {
  description = "Your IP address for SSH access (CIDR format)"
  type        = string
  default     = "0.0.0.0/0"  # ⚠️ Change this to your IP: "1.2.3.4/32"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}