#!/bin/bash
# WordPress on EC2 + RDS - Manual Installation Script
# Run on Ubuntu EC2 instance during bootstrap

# Update system
apt-get update -y

# Install Apache
apt-get install -y apache2

# Install PHP and MySQL extensions
apt-get install -y php libapache2-mod-php php-mysqlnd php-curl php-gd php-mbstring php-xml php-xmlrpc php-soap php-intl php-zip

# Enable Apache
systemctl start apache2
systemctl enable apache2

# Download WordPress
cd /tmp
wget https://wordpress.org/latest.tar.gz

# Extract
tar -xzf latest.tar.gz

# Move to web root
cp -r wordpress/* /var/www/html/

# Set permissions
chown -R www-data:www-data /var/www/html/
chmod -R 755 /var/www/html/

# Remove default page
rm /var/www/html/index.html

# Create wp-config.php from sample
cp /var/www/html/wp-config-sample.php /var/www/html/wp-config.php

# Set permissions on config
chmod 640 /var/www/html/wp-config.php

# Enable rewrite module
a2enmod rewrite

# Restart Apache
systemctl restart apache2

echo "WordPress installation complete!" > /var/log/wordpress-install.log