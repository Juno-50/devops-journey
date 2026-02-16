#!/bin/bash

# WordPress Installation Script
# Run on EC2 boot

exec > >(tee /var/log/user-data.log) 2>&1
set -x

# Update system
yum update -y

# Install dependencies
yum install -y \
    httpd \
    php php-mysqlnd php-json php-gd php-curl php-mbstring php-xml php-zip \
    mysql

# Start Apache
systemctl start httpd
systemctl enable httpd

# Download WordPress
cd /var/www/html
wget https://wordpress.org/latest.tar.gz -O wordpress.tar.gz
tar -xzf wordpress.tar.gz
mv wordpress/* .
rm -rf wordpress wordpress.tar.gz

# Set permissions
chown -R apache:apache /var/www/html
chmod -R 755 /var/www/html

# Create wp-config.php from sample
cp /var/www/html/wp-config-sample.php /var/www/html/wp-config.php

# Note: You'll need to manually configure wp-config.php or use
# SSM Parameter Store / Secrets Manager for production

echo "WordPress installed successfully at $(date)" >> /var/log/wordpress-install.log