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

## Week 2: Python + Automation 🔄 IN PROGRESS

### Day 8 - AWS CLI & Boto3 Automation ✅ COMPLETE
- [x] AWS CLI installed and configured
- [x] IAM access keys created for programmatic access
- [x] Python 3.12.10 configured
- [x] Boto3 1.42.50 installed
- [x] **Script 1:** EC2 Instance Reporter - Lists all EC2 with details, exports to CSV
- [x] **Script 2:** S3 Bucket Manager - Create, upload, download, delete buckets
- [x] **Script 3:** EC2 Controller - Start/stop/restart instances by tag
- [x] All scripts tested successfully
- [x] Full documentation and error handling
- [x] Pushed to GitHub

**Environment:**
- Python: 3.12.10
- Boto3: 1.42.50
- AWS CLI: Configured with IAM access keys
- Region: us-east-1

**Scripts Created:**
1. `ec2_reporter.py` - Inventory management with CSV export
2. `s3_manager.py` - S3 operations automation
3. `ec2_controller.py` - Instance lifecycle control by tag

**Portfolio Value:** Each script = $50-150 Upwork gig
**Tech Level:** Production-ready code, professional documentation

### Day 9 - Multi-Service Resource Reporter ✅ COMPLETE
- [x] Node.js project initialized with AWS SDK v3
- [x] Modular architecture (clients, collectors, helpers)
- [x] **aws-clients.js** - Factory for EC2, S3, RDS, Cost Explorer clients
- [x] **resource-collectors.js** - Pagination support for large inventories
- [x] **cost-collector.js** - Cost Explorer API integration
- [x] **file-helpers.js** - JSON/CSV export utilities
- [x] **generate-report.js** - Main script orchestrating all services
- [x] All scripts tested successfully
- [x] Professional documentation
- [x] Pushed to GitHub

**Technology Stack:**
- Runtime: Node.js
- Language: JavaScript (ES6+)
- AWS SDK: v3 (modular clients)
- Pattern: Async/await with parallel execution

**Output:** Multi-service reports (JSON + CSV) with cost analysis

### Day 10 - Weather Data Pipeline ✅ COMPLETE
- [x] OpenWeatherMap API integration
- [x] Multi-city weather fetching with retry logic
- [x] S3 storage (date-based structure: YYYY/MM/DD/city_HHMMSS.json)
- [x] Weather analytics (min/max/avg temperature)
- [x] Data viewer script with filtering
- [x] Scheduler for periodic execution
- [x] Comprehensive error handling + logging
- [x] Professional documentation

**Scripts Created:**
1. `weather_to_s3.py` - Main ingestion pipeline
2. `weather_analytics.py` - Statistical analysis
3. `weather_scheduler.py` - Periodic trigger
4. `view_weather_data.py` - Data browser
5. `requirements.txt` - Dependencies
6. `.env.example` - Configuration template

**Tech Stack:**
- Python 3.x with requests, python-dotenv, boto3
- OpenWeatherMap API (free tier)
- AWS S3 (date-keyed storage)
- Error handling: Retry with exponential backoff

**Portfolio Value:** Multi-service pipeline = $200-500 Upwork gig

---

## Week 2 Summary (Days 8-10) ✅ COMPLETE

| Day | Project | Status | Lines of Code |
|-----|---------|--------|----------------|
| 8 | Boto3 Scripts (EC2, S3, Controller) | ✅ | ~300 |
| 9 | Multi-Service Reporter (Node.js) | ✅ | ~400 |
| 10 | Weather Pipeline (Python) | ✅ | ~500 |
| **Total** | **3 production-ready projects** | **✅** | **~1200** |

**Deliverables:** 8 scripts, 3 README files, fully documented, all tested, pushed to GitHub.

---

### Day 11 - Serverless REST API + Scheduled Collector ✅ COMPLETE
- [x] API Gateway REST API with API key auth
- [x] Lambda handler for /cities and /weather endpoints
- [x] Scheduled collector (hourly EventBridge trigger)
- [x] S3 caching (15-minute TTL)
- [x] DynamoDB table for history
- [x] SAM infrastructure as code
- [x] Professional documentation

**Tech Stack:** Python 3.12, Lambda, API Gateway, S3, DynamoDB, SAM
**Deliverables:** weather_api.py (320 LOC), weather_to_s3.py (145 LOC), template.yaml, requirements.txt, .env.example
**Portfolio Value:** $300-500

---

### Day 12 - DynamoDB Integration + Historical Analytics ✅ COMPLETE
- [x] Enhanced collector with dual S3+DynamoDB writes
- [x] DynamoDB table design (city + timestamp keys)
- [x] Time-series weather history storage
- [x] 90-day TTL auto-cleanup
- [x] Atomic writes with error handling
- [x] Comprehensive logging

**Tech Stack:** Python 3.12, boto3, DynamoDB, CloudWatch
**Deliverables:** weather_collector_v2.py (230 LOC), comprehensive README
**Portfolio Value:** $400-600 (historical + analytics)

---

**Week 2 Complete:** Days 8-12 = 5 production projects, ~2065 LOC, all tested & documented ✅

### Day 13-14: Next Phase
- [ ] Day 13: Portfolio Website & GitHub polish
- [ ] Day 14: REST DAY + Plan Week 3 (Terraform)

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
