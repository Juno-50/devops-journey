# WordPress on EC2 + RDS MySQL

2-tier web application: WordPress web server on EC2 with managed MySQL backend on RDS.

## Architecture

- **Web Tier**: EC2 (t2.micro) in Public Subnet
- **Database Tier**: RDS MySQL (db.t3.micro) in Private Subnet
- **Networking**: VPC with Internet Gateway, Security Groups

## Quick Deploy

```bash
# Set your database password
export TF_VAR_db_password="YourSecurePassword123!"

# Initialize Terraform
cd wordPress-rds
terraform init

# Review changes
terraform plan

# Deploy (takes ~10-15 minutes for RDS)
terraform apply

# Destroy when done
terraform destroy
```

## WordPress Setup

1. Visit the EC2 public IP in browser
2. Complete WordPress installation wizard
3. Enter RDS credentials when prompted

## Cost

- EC2 t2.micro: ~$8.50/mo (or Free Tier eligible)
- RDS db.t3.micro: ~$12/mo (Free Tier: first 12 months)
- Data transfer: ~$0.09/GB out

**Total: ~$20/mo** (Free Tier: $0 for 12 months with limits)