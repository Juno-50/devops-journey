"""
Lambda function: fetch weather from OpenWeather and write snapshots to S3.
Invoke on schedule (EventBridge) or on-demand.
Uses os.environ for configuration (no dotenv).
"""

import json
import os
import re
import time
from datetime import datetime
from typing import Any

import boto3
import requests

MAX_RETRIES = 3
RETRY_BASE_DELAY = 1.0


def _get_env(name: str, default: str | None = None) -> str:
    val = os.environ.get(name, default)
    if val is None:
        raise ValueError(f"Missing required environment variable: {name}")
    return val


def _today_prefix() -> str:
    now = datetime.utcnow()
    return f"{now.year}/{now.month:02d}/{now.day:02d}/"


def _s3_key_for_city(city: str) -> str:
    now = datetime.utcnow()
    safe_city = re.sub(r"[^a-zA-Z0-9_-]", "_", city)
    return f"{_today_prefix()}{safe_city}_{now.hour:02d}{now.minute:02d}{now.second:02d}.json"


def _fetch_from_openweather(city: str, api_key: str) -> dict:
    """Fetch current weather from OpenWeather API with retries and exponential backoff."""
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}

    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(url, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                return _normalize_openweather_response(data)
            if resp.status_code in (429, 500, 502, 503):
                last_error = f"OpenWeather returned {resp.status_code}"
                if attempt < MAX_RETRIES - 1:
                    delay = RETRY_BASE_DELAY * (2**attempt)
                    time.sleep(delay)
                continue
            last_error = f"OpenWeather returned {resp.status_code}: {resp.text[:200]}"
            break
        except requests.RequestException as e:
            last_error = str(e)
            if attempt < MAX_RETRIES - 1:
                delay = RETRY_BASE_DELAY * (2**attempt)
                time.sleep(delay)

    raise RuntimeError(last_error or "OpenWeather fetch failed")


def _normalize_openweather_response(data: dict) -> dict:
    """Normalize OpenWeather API response to our schema."""
    main = data.get("main", {})
    wind = data.get("wind", {})
    weather_list = data.get("weather", [])
    condition = weather_list[0].get("description", "unknown") if weather_list else "unknown"

    return {
        "city": data.get("name", "unknown"),
        "temperature_c": round(main.get("temp", 0), 1),
        "feels_like_c": round(main.get("feels_like", 0), 1),
        "humidity": main.get("humidity", 0),
        "wind_speed_ms": round(wind.get("speed", 0), 1),
        "condition": condition,
        "last_updated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def _write_to_s3(s3_client, bucket: str, city: str, data: dict) -> str:
    """Write weather snapshot to S3. Returns the object key."""
    key = _s3_key_for_city(city)
    body = json.dumps(data, indent=2)
    s3_client.put_object(Bucket=bucket, Key=key, Body=body, ContentType="application/json")
    return key


def lambda_handler(event: dict, context: Any) -> dict:
    """
    Lambda entry point.
    Fetches weather for each city in CITIES env and writes to S3.
    """
    api_key = _get_env("OPENWEATHER_API_KEY")
    bucket = _get_env("S3_BUCKET_NAME", "weather-data-bucket-2026")
    cities_str = os.environ.get("CITIES", "London,Paris,New York")
    cities = [c.strip() for c in cities_str.split(",") if c.strip()]

    s3_client = boto3.client("s3")
    results = []

    for city in cities:
        try:
            data = _fetch_from_openweather(city, api_key)
            key = _write_to_s3(s3_client, bucket, city, data)
            results.append({"city": city, "key": key, "ok": True})
        except Exception as e:
            results.append({"city": city, "ok": False, "error": str(e)})

    return {"processed": len(results), "results": results}
