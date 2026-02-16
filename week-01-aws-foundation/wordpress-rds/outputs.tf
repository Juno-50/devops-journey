output "wordpress_url" {
  description = "URL to access WordPress"
  value       = "http://${aws_instance.wordpress.public_ip}"
}

output "database_endpoint" {
  description = "RDS MySQL endpoint"
  value       = aws_db_instance.wordpress.endpoint
  sensitive   = true
}

output "ssh_command" {
  description = "Command to SSH into EC2"
  value       = "ssh -i your-key.pem ec2-user@${aws_instance.wordpress.public_ip}"
}