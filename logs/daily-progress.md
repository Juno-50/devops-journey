# Daily Progress Log

## Week 1: AWS Foundation ✅ COMPLETE

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
- [x] Created VPC: juno-first-vpc (10.0.0.0/16)
- [x] Public Subnet: 10.0.1.0/24
- [x] Private Subnet: 10.0.2.0/24
- [x] Internet Gateway attached
- [x] Route tables configured
- [x] Tested connectivity

### Day 5 - Practice Exam
- [x] AWS Skill Builder exam
- [x] Identified weak areas
- [x] Created flashcards

### Day 6 - Multi-tier Architecture ✅ COMPLETE

#### Resources Deployed:
| Resource | Details |
|----------|---------|
| VPC | juno-first-vpc (10.0.0.0/16) |
| Public Subnet | 10.0.1.0/24 |
| Private Subnet | 10.0.2.0/24 |
| EC2 Instance | i-0e76637bec7c2d75a (t2.micro, Ubuntu 22.04) |
| EC2 Public IP | 50.17.141.215 |
| EC2 Private IP | 10.0.1.163 |
| RDS Instance | wordpress-db (db.t3.micro, MySQL 8.0) |
| RDS Endpoint | wordpress-db.c0dyeuwaaufo.us-east-1.rds.amazonaws.com |
| Security Groups | wordpress-web-sg, wordpress-db-sg |

#### Configuration:
- Web server in public subnet with Apache + PHP
- RDS in private subnet with no public access
- Security groups: layered defense (DB only accessible from web tier)
- WordPress deployment via SSH and browser setup

#### Testing & Validation ✅ ALL PASSED:
- [x] Website accessible from internet (http://50.17.141.215)
- [x] WordPress admin panel loads (/wp-admin/)
- [x] Can create and publish posts
- [x] Database connectivity verified (MySQL CLI from EC2)
- [x] Security groups tested (HTTP open, SSH restricted to my IP)
- [x] RDS inaccessible from internet (private subnet)
- [x] Test post created: "Hello from AWS!" - confirmed in RDS
- [x] Architecture diagram documented
- [x] Access credentials saved securely
- [x] All screenshots captured

**Cost: $0 (Free Tier eligible)**

---

## Week 2: Python + Automation 🔄 PENDING

### Day 8-13
- [ ] Python crash course
- [ ] Boto3 setup and configuration
- [ ] Resource monitoring scripts
- [ ] Lambda functions
- [ ] Cost tracking automation

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
