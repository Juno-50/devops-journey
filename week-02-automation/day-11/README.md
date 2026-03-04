# Day 11: Serverless Weather API + Scheduled Collector

## Project Overview

**Weather API with automatic hourly data collection**

Two Lambda functions working together:
1. **REST API** - On-demand weather via HTTP endpoints
2. **Scheduled Collector** - Hourly cache updates

**Live Endpoints:**
- `GET /cities` - List available cities
- `GET /weather?city=Tokyo` - Get weather data

**Cities:** Tokyo, New York, London, Sydney, Paris

**Cost:** ~$0.03/month | **Architecture:** Serverless | **Auth:** API Key

---

## Architecture

```
User Request → API Gateway → Lambda (weather_api.py)
                                ↓
                          S3 Cache (15 min TTL)
                                ↑
Hourly Trigger → Lambda (weather_to_s3.py)
```

**Benefits:**
- Fast API responses (~50ms from cache)
- Fresh data (updated hourly)
- Reduced external API calls
- Historical data storage

---

## Deployment

### Prerequisites
- AWS CLI configured
- SAM CLI installed
- OpenWeatherMap API key
- S3 bucket created

### Quick Deploy

```bash
# 1. Build
sam build

# 2. Deploy
sam deploy --guided

# Answer prompts:
# Stack name: weather-api-complete
# OpenWeatherApiKey: [your key]
# Cities: Tokyo,New York,London,Sydney,Paris
# CacheTtlSeconds: 900
```

### Get API Credentials

```bash
# Get endpoint
sam list stack-outputs --stack-name weather-api-complete

# Get API key
# AWS Console → API Gateway → WeatherApi → API Keys → Show
```

---

## Usage

### Test API

```bash
# List cities
curl -H "x-api-key: YOUR_KEY" \
  "https://YOUR_ENDPOINT/prod/cities"

# Get weather
curl -H "x-api-key: YOUR_KEY" \
  "https://YOUR_ENDPOINT/prod/weather?city=Tokyo"
```

### Monitor Collector

```bash
# View logs
sam logs --stack-name weather-api-complete \
  --name WeatherCollectorFunction --tail

# Check S3 cache
aws s3 ls s3://weather-data-bucket-2026/
```

---

## Files

```
day-11/
├── template.yaml              # SAM template (both functions)
├── lambda/
│   ├── weather_api.py         # REST API handler
│   └── weather_to_s3.py       # Scheduled collector
├── requirements.txt           # Dependencies
├── .env.example               # Configuration template
└── README.md                  # This file
```

---

## Key Learnings

**Day 11 Skills:**
- Serverless API Gateway setup
- Lambda function deployment with SAM
- CloudWatch Events scheduling
- S3 caching strategy
- API key authentication
- Multi-function architecture
- Infrastructure as Code (IaC)

**AWS Services Used:**
- Lambda (2 functions)
- API Gateway (REST API)
- CloudWatch Events (scheduler)
- S3 (cache storage)
- IAM (automatic roles)
- CloudWatch Logs (monitoring)

---

## Cost Breakdown

**Monthly (estimated):**
- Lambda API: $0.001
- Lambda Collector: $0.020
- API Gateway: $0.010
- S3: $0.001
- OpenWeather API: $0 (free tier)

**Total: ~$0.03/month**

---

## Updating

```bash
# After code changes
sam build && sam deploy

# Update just code (faster)
sam deploy --no-confirm-changeset
```

---

## Troubleshooting

**API returns 403:** Missing API key header

**Collector not running:** Check CloudWatch Events rule enabled

**Old data returned:** Cache TTL not expired yet (15 min)

---

## Portfolio Value

**What This Demonstrates:**
- Professional serverless architecture
- Event-driven automation
- RESTful API design
- Cache optimization
- Cost-effective solutions
- Production deployment skills

**Upwork Value:** $300-500 for similar projects

---

## Next Steps
- Add more endpoints (/forecast, /historical)
- Implement rate limiting
- Add custom domain name
- Create CloudWatch dashboard
- Add error alerting (SNS)
- Extend to more cities

---

**Stack Name:** weather-api-complete  
**Deployment Method:** AWS SAM  
**Date:** February 19, 2026
