# Daily Progress Log

## Week 1: AWS Foundation ✓

### Day 1 - AWS Account Setup
- [x] Created AWS Free Tier account
- [x] Set up billing alerts ($5, $10 thresholds)
- [x] Enabled MFA on root account
- [x] Created IAM user with admin access

### Day 2 - First EC2 Instance
- [x] Launched t2.micro Ubuntu instance
- [x] SSH into instance
- [x] Installed nginx web server
- [x] Accessed via public IP

### Day 3 - S3 Static Website
- [x] Created S3 bucket with website hosting
- [x] Uploaded HTML/CSS files
- [x] Configured bucket policy
- [x] Live site accessible

### Day 4 - VPC from Scratch
- [x] Created custom VPC
- [x] Public and private subnets
- [x] Route tables and Internet Gateway
- [x] Tested connectivity

### Day 5 - Practice Exam
- [x] AWS Skill Builder exam
- [x] Identified weak areas
- [x] Created flashcards

### Day 6 - Multi-tier Architecture - WordPress on RDS ✅ COMPLETE
- [x] Created RDS MySQL database (wordpress-db)
- [x] Configured DB subnet group with private subnets
- [x] Created security groups (wordpress-web-sg, wordpress-db-sg)
- [x] Launched EC2 t2.micro in public subnet
- [x] Deployed WordPress with Apache + PHP
- [x] Configured wp-config.php with RDS endpoint
- [x] Verified database connectivity
- [x] Created test post confirming data persistence

**Resources Deployed:**
- RDS Endpoint: `wordpress-db.c0dyeuwaaufo.us-east-1.rds.amazonaws.com`
- EC2 Instance ID: `i-0e76637bec7c2d75a`
- EC2 Public IP: `50.17.141.215`
- EC2 Private IP: `10.0.1.163`
- WordPress URL: `http://50.17.141.215/wp-admin/`
- DB Username: admin

**Architecture:** 2-tier multi-AZ deployment with web tier in public subnet and database tier in private subnet. Security groups layered for defense in depth.

## Week 2: Python + Automation

### Day 8-13
- [ ] Python crash course
- [ ] Boto3 scripting
- [ ] Resource monitoring
- [ ] Lambda functions

---

## Notes Template

```
### Day X - [Date] - [Topic]

**Morning Session:**
- Activity:
- Key Learnings:
- Blockers:

**Afternoon Session:**
- Activity:
- Code Written:
- Errors Encountered:

**Deliverables:**
- [ ] Item 1
- [ ] Item 2

**Reflection:**
```
