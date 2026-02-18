# Day 10: Weather Data Pipeline

Production-style Python pipeline fetching OpenWeatherMap API data to S3 with scheduling and analytics.

---

## Architecture

```
OpenWeatherMap API → Python Pipeline → S3 Storage → Analytics/Viewer
                          │
                    Scheduler (Periodic)
```

## Project Structure

| File | Purpose |
|------|---------|
| `weather_to_s3.py` | Main ingestion pipeline |
| `view_weather_data.py` | Browse and inspect stored JSON objects |
| `weather_analytics.py` | Compute temperature statistics |
| `weather_scheduler.py` | Periodically trigger pipeline |
| `requirements.txt` | Python dependencies |
| `.env.example` | Configuration template |

## Features

- **Config-driven**: `.env` file using `python-dotenv`
- **Weather ingestion**: Multi-city current weather via OpenWeatherMap API
- **S3 storage**: Date-based key structure (`YYYY/MM/DD/city_HHMMSS.json`)
- **Robust error handling**: Retries with exponential backoff
- **Logging**: Run summaries and S3 logs

## S3 Data Structure

```
s3://weather-data-bucket-2026/
├── data/
│   └── 2026/
│       └── 02/
│           └── 18/
│               ├── New_york_183015.json
│               ├── Tokyo_183020.json
│               └── London_183025.json
```

### JSON Contents
- Temperature (Celsius)
- Humidity
- Pressure
- Wind speed/direction
- Weather conditions
- Coordinates
- Timestamp

## Prerequisites

- Python 3.9+
- OpenWeatherMap API key
- S3 bucket: `weather-data-bucket-2026`
- AWS credentials (via default credential chain)

## Installation

```bash
cd day-10
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API key and settings
```

## Usage

```bash
# Run ingestion pipeline
python weather_to_s3.py

# View stored data
python view_weather_data.py --city New_york --date 2026-02-18

# Run analytics
python weather_analytics.py --start-date 2026-02-01 --end-date 2026-02-18

# Start scheduler
python weather_scheduler.py
```

## Use Cases

- Weather trend analysis
- Climate research
- Historical data archiving
- IoT sensor integration
- API data backup

---

**Status:** Scripts in development
