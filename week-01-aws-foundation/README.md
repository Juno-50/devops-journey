# Week 1: AWS Foundation (Manual Deployment)

All labs completed using AWS Console and CLI — no Terraform. Infrastructure as Code comes in Week 3.

---

## Day 1: AWS Account Setup ✅
- Free Tier account created
- Billing alerts: $5, $10 thresholds
- MFA enabled on root
- IAM admin user created

## Day 2: First EC2 Instance ✅
- Launched t2.micro Ubuntu
- SSH access configured
- Nginx installed and running
- Public IP accessible

## Day 3: S3 Static Website ✅
- S3 bucket with website hosting
- HTML/CSS uploaded
- Public bucket policy
- Live site URL

## Day 4: VPC from Scratch ✅
- **VPC**: juno-first-vpc (10.0.0.0/16)
- **Public subnet**: 10.0.1.0/24
- **Private subnet**: 10.0.2.0/24
- Internet Gateway attached
- Route tables configured

## Day 5: Practice Exam ✅
- AWS Skill Builder exam
- Weak areas identified
- Flashcards created

## Day 6: Multi-tier Architecture ✅ COMPLETE

### What Was Built
2-tier WordPress application with separation of concerns:

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
    │       - WordPress files
    │       - Public IP: 50.17.141.215
    │
    └── Private Subnet (10.0.2.0/24)
        └── RDS: wordpress-db
            - MySQL 8.0
            - Managed by AWS
            - No public access
```

### Resources Created

| Resource | Type | Details |
|----------|------|---------|
| VPC | juno-first-vpc | 10.0.0.0/16 |
| Public Subnet | subnet-xxx | 10.0.1.0/24 |
| Private Subnet | subnet-xxx | 10.0.2.0/24 |
| EC2 Instance | i-0e76637bec7c2d75a | t2.micro, Ubuntu 22.04 |
| RDS Instance | wordpress-db | db.t3.micro, MySQL 8.0 |
| Security Group | wordpress-web-sg | HTTP, HTTPS, SSH |
| Security Group | wordpress-db-sg | MySQL from web-sg only |
| DB Subnet Group | wordpress-db-subnet-group | Private subnets |

### Deployment Steps (Manual)

1. **Create DB Subnet Group**
   - RDS Console → Subnet Groups → Create
   - Selected private subnets in juno-first-vpc

2. **Create Security Groups**
   - `wordpress-db-sg`: MySQL (3306) from web tier only
   - `wordpress-web-sg`: HTTP (80), HTTPS (443), SSH (22) from my IP

3. **Launch RDS Database**
   - Engine: MySQL 8.0
   - Instance: db.t3.micro (Free Tier)
   - Storage: 20 GB
   - Subnet: Private subnet group
   - Public access: NO
   - Endpoint: `wordpress-db.c0dyeuwaaufo.us-east-1.rds.amazonaws.com`

4. **Launch EC2 Web Server**
   - AMI: Ubuntu Server 22.04 LTS
   - Type: t2.micro (Free Tier)
   - Subnet: Public subnet
   - Auto-assign public IP: YES
   - Security group: wordpress-web-sg
   - User data script installed Apache + PHP + WordPress

5. **Configure WordPress**
   - SSH into EC2
   - Edit wp-config.php with RDS credentials
   - Complete installation wizard

### Access Information

```
WordPress URL:     http://50.17.141.215/wp-admin/
RDS Endpoint:      wordpress-db.c0dyeuwaaufo.us-east-1.rds.amazonaws.com
RDS Port:          3306
RDS DB Name:       wordpress
RDS Username:      admin
EC2 Public IP:     50.17.141.215
EC2 Private IP:    10.0.1.163
Instance ID:       i-0e76637bec7c2d75a
SSH Command:       ssh -i first-ec-key.pem ubuntu@50.17.141.215
```

### Testing & Validation ✅

- [x] Website accessible from internet
- [x] WordPress admin panel loads
- [x] Can create and publish posts
- [x] Database connectivity verified via MySQL client
- [x] Security groups tested (HTTP open, SSH restricted)
- [x] RDS in private subnet (no public access)
- [x] Test post created and retrieved from database
- [x] Architecture diagram documented

### Security Layers Applied

1. **Network Layer**: VPC segmentation (public/private subnets)
2. **Security Group Layer**: wordpress-web-sg and wordpress-db-sg
3. **Access Control**: SSH restricted to my IP only
4. **Database Security**: RDS in private subnet, no public access
5. **Encryption**: RDS storage encrypted at rest

### Cost

**Free Tier (First Year):** $0
- EC2 t2.micro: 750 hrs/month free
- RDS db.t3.micro: 750 hrs/month free
- Storage: Within limits

**After Free Tier:** ~$23/month

