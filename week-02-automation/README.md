# Week 2: Python + AWS Automation

**Status:** Day 8 Complete ✅ (5 days remaining)

---

## Day 8: AWS CLI & Boto3 ✅ COMPLETE

### Accomplishments
- AWS CLI configured with IAM access keys
- Python 3.12.10 + Boto3 1.42.50 environment setup
- 3 production-ready automation scripts created
- All scripts tested and documented

### Scripts Created

#### 1. EC2 Instance Reporter (`ec2_reporter.py`)
**Purpose:** Lists all EC2 instances with key details and exports to CSV

**Features:**
- Shows: Name, Instance ID, State, Type, Public/Private IPs
- Exports to `ec2_instances.csv` for reporting
- Handles missing name tags gracefully
- Formatted console table output

**Usage:**
```bash
python ec2_reporter.py
```

**Use Case:** Inventory management, resource auditing, cost tracking

---

#### 2. S3 Bucket Manager (`s3_manager.py`)
**Purpose:** Complete S3 bucket lifecycle management

**Features:**
- Create buckets (globally unique names)
- Upload files with size validation
- List bucket contents
- Download files
- Delete buckets (with object cleanup)

**Usage:**
```bash
python s3_manager.py
# Interactive demo creates, uploads, lists, downloads, and cleans up
```

**Use Case:** Automated backups, file distribution, content deployment

---

#### 3. EC2 Controller (`ec2_controller.py`)
**Purpose:** Instance lifecycle control by tags

**Features:**
- Start/stop/restart instances by tag filter
- Dry-run mode for testing
- Interactive confirmation
- Waits for state transitions
- Error handling and logging

**Usage:**
```bash
# Stop dev instances
python ec2_controller.py stop --tag Environment=test

# Start test servers
python ec2_controller.py start --tag Name=test-server

# Preview without executing
python ec2_controller.py restart --tag Project=Demo --dry-run
```

**Use Case:** Cost savings (stop dev servers overnight), maintenance windows

---

### Technical Stack

| Component | Version | Purpose |
|-----------|---------|---------|
| Python | 3.12.10 | Language |
| Boto3 | 1.42.50 | AWS SDK |
| AWS CLI | Latest | Credential configuration |
| Region | us-east-1 | Primary deployment |

---

### Key Concepts Learned

**Boto3 Patterns:**
- `boto3.client()` for service operations
- Response structure parsing (nested dictionaries)
- Error handling with try/except
- Paginated results handling

**AWS Authentication:**
- IAM access keys (programmatic access)
- Default credential chain (environment variables, config files)
- Security best practices

---

### Deliverables

✅ AWS CLI configured
✅ Boto3 installed and tested
✅ 3 automation scripts created
✅ All scripts tested and working
✅ Professional README documented
✅ Code pushed to GitHub

---

## Day 9: Multi-Service Resource Reporter ✅ COMPLETE

### Accomplishments
- Node.js project with AWS SDK v3
- Modular architecture with separation of concerns
- Multi-service resource collection (EC2, S3, RDS)
- Cost Explorer API integration
- JSON and CSV report generation

### Scripts Created
| File | Purpose |
|------|---------|
| `generate-report.js` | Main orchestration script |
| `aws-clients.js` | AWS service client factory |
| `resource-collectors.js` | EC2, S3, RDS collection with pagination |
| `cost-collector.js` | Cost Explorer API for monthly costs |
| `file-helpers.js` | JSON/CSV file utilities |

### Usage
```bash
cd day-09
npm install
node generate-report.js
```

### Output
- `reports/aws-resources.json` - Complete inventory
- `reports/ec2-instances.csv` - EC2 details
- `reports/s3-buckets.csv` - S3 bucket list
- `reports/rds-instances.csv` - RDS databases
- `reports/service-costs.csv` - Cost breakdown

### Technical Stack
- Runtime: Node.js
- Language: JavaScript (ES6+)
- AWS SDK: v3 (modular clients)
- Pattern: Async/await with Promise.all

---

## Day 10-13: Planned Work

### Day 10: Lambda Functions
- Serverless automation
- Event-driven architectures
- API Gateway integration

### Day 11: Advanced Cost Monitoring
- Budget alerts
- Resource optimization recommendations

### Day 12: Infrastructure Testing
- Validation scripts
- Compliance checking

### Day 13: Capstone Project
- Multi-service automation
- Production-ready pipeline
