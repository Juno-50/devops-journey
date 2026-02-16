# WordPress on EC2 + RDS MySQL (Manual Deployment)

2-tier web application deployed manually via AWS Console and SSH.

## Architecture

```
Internet
    │
Internet Gateway
    │
juno-first-vpc (10.0.0.0/16)
    │
    ├── Public Subnet (10.0.1.0/24)
    │   └── EC2: wordpress-web-server
    │       - Apache + PHP
    │       - WordPress
    │       - Public IP: 50.17.141.215
    │
    └── Private Subnet (10.0.2.0/24)
        └── RDS: wordpress-db
            - MySQL 8.0
            - No public access
```

## Resources

| Resource | Identifier | Details |
|----------|------------|---------|
| VPC | juno-first-vpc | 10.0.0.0/16 |
| EC2 Instance | i-0e76637bec7c2d75a | t2.micro, Ubuntu 22.04 |
| RDS | wordpress-db | db.t3.micro, MySQL 8.0 |
| RDS Endpoint | wordpress-db.c0dyeuwaaufo.us-east-1.rds.amazonaws.com | Port 3306 |

## Deployment Steps

### 1. Create DB Subnet Group
- RDS Console → Subnet Groups → Create
- Name: `wordpress-db-subnet-group`
- VPC: `juno-first-vpc`
- Subnets: Private subnets only

### 2. Create Security Groups

**wordpress-db-sg:**
- Inbound: MySQL (3306) from wordpress-web-sg only
- Outbound: All traffic

**wordpress-web-sg:**
- Inbound: HTTP (80) from 0.0.0.0/0
- Inbound: HTTPS (443) from 0.0.0.0/0  
- Inbound: SSH (22) from YOUR_IP/32
- Outbound: All traffic

### 3. Launch RDS
- Engine: MySQL 8.0
- Instance: db.t3.micro (Free Tier)
- Storage: 20 GB
- Subnet: wordpress-db-subnet-group
- Public access: NO
- Security: wordpress-db-sg

### 4. Launch EC2
- AMI: Ubuntu Server 22.04 LTS
- Type: t2.micro
- Subnet: Public subnet (auto-assign IP)
- Security: wordpress-web-sg
- User data: See `user-installation-script.sh`

### 5. Configure WordPress
SSH into EC2:
```bash
ssh -i first-ec-key.pem ubuntu@50.17.141.215
```

Edit wp-config.php:
```bash
sudo nano /var/www/html/wp-config.php
```

Add RDS credentials (see `wp-config-example.php`):
- DB_NAME: wordpress
- DB_USER: admin
- DB_PASSWORD: YOUR_PASSWORD
- DB_HOST: wordpress-db.c0dyeuwaaufo.us-east-1.rds.amazonaws.com

### 6. Complete Setup
Visit: http://50.17.141.215/wp-admin/

## Scripts in This Folder

| File | Purpose |
|------|---------|
| `user-installation-script.sh` | Bootstrap script for EC2 userdata |
| `wp-config-example.php` | Template for WordPress database config |

## Access

- WordPress: http://50.17.141.215/wp-admin/
- SSH: `ssh -i first-ec-key.pem ubuntu@50.17.141.215`
- RDS: Endpoint (no direct access, via EC2 only)

## Cost

Free Tier: $0/month
After: ~$23/month
