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
python ec2_controller.py stop --tag Environment= est

# Start test servers
python ec2_controller.py start --tag Name=WebServer

```


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

**AI-Assisted Development:**
- Prompt engineering for code generation
- Code review and customization
- Understanding vs. memorizing

**Boto3 Patterns:**
- `boto3.client()` for service operations
- Response structure parsing (nested dictionaries)
- Error handling with try/except
- Paginated results handling

**AWS Authentication:**
- IAM access keys (programmatic access)
- Default credential chain
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

## Day 9-13: Planned Work

### Day 9: Resource Reporter
- Multi-service inventory (EC2, S3, RDS, Lambda)
- Cost analysis integration
- Scheduled execution

### Day 10: Lambda Functions
- Serverless automation
- Event-driven architectures
- API Gateway integration

### Day 11: Cost Monitoring
- AWS Cost Explorer API
- Budget alerts
- Resource optimization recommendations

### Day 12: Infrastructure Testing
- Validation scripts
- Compliance checking
- Security auditing

### Day 13: Capstone Project
- Multi-service automation
- Integration of all learned skills
- Production-ready pipeline

---

## Upwork Offerings

Based on Day 8 skills, you can now offer:

| Service | Price Range | Skills |
|---------|-------------|--------|
| AWS EC2 Automation Script | $75-150 | Boto3, EC2 API |
| S3 Bucket Management Tool | $50-100 | S3, Python |
| Instance Scheduler | $100-200 | Lambda/EventBridge |
| AWS Resource Inventory | $150-300 | Multi-service |

**Competitive Advantage:**
- AI-assisted development = faster delivery
- Production-ready code with error handling
- Professional documentation
- GitHub portfolio visible to clients
