"""weather_to_s3.py
Fetch current weather data for a list of cities from OpenWeatherMap and upload each city's result as a JSON object into an S3 bucket.

Configuration is provided via environment variables loaded from a .env file:
- OPENWEATHER_API_KEY
- S3_BUCKET_NAME
- CITIES (comma-separated list of city names)
- Optional: S3_LOG_PREFIX

AWS credentials are resolved via the default AWS credential chain (AWS Toolkit, env vars, shared config/credentials files, IAM role, etc.).
"""

from __future__ import annotations
import json
import logging
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, TypedDict

import boto3
from botocore.exceptions import BotoCoreError, ClientError
import requests
from requests import Response
from dotenv import load_dotenv


# ---------------------------
# Configuration & Data Models
# ---------------------------

@dataclass
class Config:
    """Holds configuration loaded from environment variables."""
    openweather_api_key: str
    s3_bucket_name: str
    cities: List[str]
    s3_log_prefix: Optional[str] = None


class WeatherData(TypedDict):
    """Structured weather payload to store in S3."""
    city: str
    country: Optional[str]
    coordinates: Dict[str, float]
    temperature_c: float
    feels_like_c: float
    humidity: int
    pressure_hpa: int
    weather_main: str
    weather_description: str
    wind_speed_ms: float
    timestamp_utc: str
    raw_source: Dict[str, object]


class WeatherAPIError(Exception):
    """Custom exception for weather API failures."""
    def __init__(self, message: str, status_code: Optional[int] = None, retriable: bool = False) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.retriable = retriable


# -------------
# Setup Logging
# -------------

def setup_logging() -> None:
    """Configure root logger for timestamped console output."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


# ------------------------
# Environment / .env Logic
# ------------------------

def load_env_config() -> Config:
    """Load configuration from .env / environment variables."""
    load_dotenv()
    api_key = os.getenv("OPENWEATHER_API_KEY")
    bucket = os.getenv("S3_BUCKET_NAME")
    cities_raw = os.getenv("CITIES", "")
    log_prefix = os.getenv("S3_LOG_PREFIX")

    missing: List[str] = []
    if not api_key:
        missing.append("OPENWEATHER_API_KEY")
    if not bucket:
        missing.append("S3_BUCKET_NAME")
    if not cities_raw.strip():
        missing.append("CITIES")

    if missing:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing)}. "
            "Ensure they are set in your .env file."
        )

    cities = [c.strip() for c in cities_raw.split(",") if c.strip()]
    if not cities:
        raise RuntimeError("No valid cities provided in CITIES environment variable.")

    return Config(
        openweather_api_key=api_key,
        s3_bucket_name=bucket,
        cities=cities,
        s3_log_prefix=log_prefix or None,
    )


# ----------------------
# Weather API Integration
# ----------------------

def kelvin_to_celsius(kelvin: float) -> float:
    """Convert Kelvin to Celsius."""
    return kelvin - 273.15


def _classify_retriable(status_code: Optional[int]) -> bool:
    """Decide if an HTTP status code should be retried."""
    if status_code is None:
        return True
    if status_code == 429:
        return True
    if 500 <= status_code <= 599:
        return True
    return False


def call_openweather_api(city: str, api_key: str, timeout_seconds: int = 10) -> Response:
    """HTTP request to OpenWeatherMap Current Weather API."""
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key}

    try:
        resp = requests.get(base_url, params=params, timeout=timeout_seconds)
    except requests.exceptions.RequestException as exc:
        raise WeatherAPIError(
            f"Network error while calling OpenWeather for city '{city}': {exc}",
            status_code=None, retriable=True,
        ) from exc

    if not (200 <= resp.status_code < 300):
        retriable = _classify_retriable(resp.status_code)
        message = f"HTTP {resp.status_code} from OpenWeather for city '{city}'"
        try:
            body = resp.json()
            if isinstance(body, dict) and "message" in body:
                message += f": {body['message']}"
        except Exception:
            pass
        raise WeatherAPIError(message=message, status_code=resp.status_code, retriable=retriable)

    return resp


def parse_weather_response(city: str, resp: Response) -> WeatherData:
    """Convert OpenWeather JSON response to WeatherData."""
    try:
        data = resp.json()
    except ValueError as exc:
        raise WeatherAPIError(f"Failed to parse JSON for city '{city}': {exc}", retriable=True) from exc

    try:
        main = data["main"]
        wind = data.get("wind", {})
        weather_list = data.get("weather", [])
        weather_entry = weather_list[0] if weather_list else {}
        temp_k = float(main["temp"])
        feels_k = float(main.get("feels_like", temp_k))

        result: WeatherData = {
            "city": data.get("name") or city,
            "country": (data.get("sys") or {}).get("country"),
            "coordinates": {
                "lat": float((data.get("coord") or {}).get("lat", 0.0)),
                "lon": float((data.get("coord") or {}).get("lon", 0.0)),
            },
            "temperature_c": kelvin_to_celsius(temp_k),
            "feels_like_c": kelvin_to_celsius(feels_k),
            "humidity": int(main.get("humidity", 0)),
            "pressure_hpa": int(main.get("pressure", 0)),
            "weather_main": str(weather_entry.get("main", "")),
            "weather_description": str(weather_entry.get("description", "")),
            "wind_speed_ms": float(wind.get("speed", 0.0)),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "raw_source": {"id": data.get("id"), "dt": data.get("dt")},
        }
    except (KeyError, TypeError, ValueError) as exc:
        raise WeatherAPIError(f"Unexpected response structure for city '{city}': {exc}", retriable=False) from exc

    return result


def fetch_weather_with_retry(
    city: str, config: Config, max_attempts: int = 3, initial_backoff_seconds: float = 1.0
) -> Optional[WeatherData]:
    """Fetch weather with retry logic and exponential backoff."""
    attempt = 0
    backoff = initial_backoff_seconds
    while attempt < max_attempts:
        attempt += 1
        try:
            logging.info("Fetching weather for '%s' (attempt %d/%d)", city, attempt, max_attempts)
            resp = call_openweather_api(city, config.openweather_api_key)
            return parse_weather_response(city, resp)
        except WeatherAPIError as exc:
            logging.error(
                "Weather API error for '%s' (attempt %d/%d): %s (status=%s, retriable=%s)",
                city, attempt, max_attempts, exc, getattr(exc, "status_code", None), getattr(exc, "retriable", False)
            )
            if not getattr(exc, "retriable", False):
                return None
            if attempt < max_attempts:
                time.sleep(backoff)
                backoff *= 2
        except Exception as exc:
            logging.exception("Unexpected error fetching weather for '%

def build_s3_client():
    """Build an S3 client using default AWS credential chain."""
    return boto3.client("s3")


def normalize_city_for_key(city: str) -> str:
    """Normalize city name for S3 key. Example: 'New York' -> 'new_york'"""
    return city.strip().replace(" ", "_").lower()


def build_s3_key(city: str, ts: datetime) -> str:
    """Build S3 key: YYYY/MM/DD/city_HHMMSS.json"""
    date_part = ts.strftime("%Y/%m/%d")
    time_part = ts.strftime("H%M%S")
    city_part = normalize_city_for_key(city)
    return f"{date_part}/{city_part}_{time_part}.json"


def upload_to_s3(client, bucket: str, key: str, payload: Dict[str, object]) -> bool:
    """Upload JSON payload to S3."""
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    try:
        client.put_object(Bucket=bucket, Key=key, Body=body, ContentType="application/json")
        logging.info("Uploaded to s3://%s/%s", bucket, key)
        return True
    except (ClientError, BotoCoreError) as exc:
        logging.error("Failed to upload to s3://%s/%s: %s", bucket, key, exc)
        return False


def process_cities(config: Config, client) -> Dict[str, object]:
    """Fetch weather for all cities and upload to S3."""
    total = len(config.cities)
    success_count = 0
    failure_count = 0
    temps = []
    failures = []

    for city in config.cities:
        logging.info("Processing city: %s", city)
        weather = fetch_weather_with_retry(city, config)
        if weather is None:
            failure_count += 1
            failures.append(city)
            continue

        ts = datetime.now(timezone.utc)
        key = build_s3_key(city, ts)
        uploaded = upload_to_s3(client, config.s3_bucket_name, key, weather)

        if uploaded:
            success_count += 1
            temps.append(weather["temperature_c"])
        else:
            failure_count += 1
            failures.append(city)

    summary = {
        "total_cities": total,
        "success_count": success_count,
        "failure_count": failure_count,
        "min_temp_c": min(temps) if temps else None,
        "max_temp_c": max(temps) if temps else None,
        "avg_temp_c": sum(temps) / len(temps) if temps else None,
        "failures": failures,
    }
    return summary


def main() -> int:
    """Main entry point."""
    setup_logging()
    logging.info("Starting weather_to_s3 run.")

    try:
        config = load_env_config()
    except Exception as exc:
        logging.error("Failed to load configuration: %s", exc)
        return 1

    logging.info("Loaded config for %d cities, bucket='%s'", len(config.cities), config.s3_bucket_name)

    try:
        s3_client = build_s3_client()
    except Exception as exc:
        logging.error("Failed to create S3 client: %s", exc)
        return 1

    summary = process_cities(config, s3_client)
    logging.info("Run summary: %s", json.dumps(summary, indent=2, default=str))

    if summary["failure_count"] > 0:
        logging.warning("Completed with %d/%d failures.", summary["failure_count"], summary["total_cities"])
        return 1

    logging.info("Completed successfully: all %d cities processed.", summary["total_cities"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
