# Day 9: Multi-Service Resource Reporter

Multi-service AWS inventory tool with cost analysis using AWS SDK for JavaScript v3.

## Architecture

Modular design separating concerns:
- `aws-clients.js` - AWS service client factory
- `resource-collectors.js` - Resource gathering logic
- `cost-collector.js` - Cost Explorer integration
- `file-helpers.js` - Report output utilities
- `generate-report.js` - Main orchestration

## Scripts

| File | Purpose |
|------|---------|
| `generate-report.js` | Main entry point - generates JSON and CSV reports |
| `aws-clients.js` | Factory functions for AWS service clients (EC2, S3, RDS, Cost Explorer) |
| `resource-collectors.js` | Collects EC2 instances, S3 buckets, RDS instances with pagination |
| `cost-collector.js` | Fetches current month costs from Cost Explorer API |
| `file-helpers.js` | Utilities for writing JSON/CSV files |

## Installation

```bash
cd day-09
npm install
```

Dependencies:
- `@aws-sdk/client-ec2` - EC2 operations
- `@aws-sdk/client-s3` - S3 operations  
- `@aws-sdk/client-rds` - RDS operations
- `@aws-sdk/client-cost-explorer` - Cost analysis

## Usage

```bash
# Generate report for current region
node generate-report.js

# Generate report for specific region
REPORT_REGION=eu-west-2 node generate-report.js
```

## Output

Creates `reports/` folder with:
- `aws-resources.json` - Complete resource inventory (JSON)
- `ec2-instances.csv` - EC2 instance details
- `s3-buckets.csv` - S3 bucket list with regions
- `rds-instances.csv` - RDS database instances
- `service-costs.csv` - Current month costs by service

## Features

- Multi-service inventory (EC2, S3, RDS)
- Cost analysis via Cost Explorer API
- Automatic pagination for large inventories
- CSV export for spreadsheet analysis
- Region-aware S3 bucket locations
- Tag normalization across resources
- Error handling for each service

## Technical Stack

- **Runtime:** Node.js
- **Language:** JavaScript (ES6+)
- **AWS SDK:** v3 (modular clients)
- **Pattern:** Async/await with Promise.all for parallel execution

## Example Output

```bash
$ node generate-report.js
Generating AWS resource report for region us-east-1...
Report generated in ./reports

$ ls reports/
aws-resources.json
ec2-instances.csv
s3-buckets.csv
rds-instances.csv
service-costs.csv
```

## Use Cases

- Monthly resource audits
- Cost breakdown by service
- Compliance reporting
- Resource optimization analysis
