"""
AWS Lambda handler for the Weather API.
Serves GET /weather and GET /cities via API Gateway REST API.
Uses S3 for caching and OpenWeather API as fallback.
"""

import json
import os
import re
import time
from datetime import datetime
from typing import Any

import boto3
import requests

# Default cache TTL: 15 minutes
DEFAULT_CACHE_TTL_SECONDS = 900

# OpenWeather retry config
MAX_RETRIES = 3
RETRY_BASE_DELAY = 1.0


def _success(data: Any, status_code: int = 200) -> dict:
    """Return a successful API Gateway response."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({"ok": True, "data": data}),
    }


def _error(code: str, message: str, status_code: int = 500) -> dict:
    """Return an error API Gateway response."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({"ok": False, "error": {"code": code, "message": message}}),
    }


def _get_env(name: str, default: str | None = None) -> str:
    val = os.environ.get(name, default)
    if val is None:
        raise ValueError(f"Missing required environment variable: {name}")
    return val


def _get_cache_ttl() -> int:
    try:
        return int(os.environ.get("CACHE_TTL_SECONDS", DEFAULT_CACHE_TTL_SECONDS))
    except ValueError:
        return DEFAULT_CACHE_TTL_SECONDS


def _today_prefix() -> str:
    now = datetime.utcnow()
    return f"{now.year}/{now.month:02d}/{now.day:02d}/"


def _s3_key_for_city(city: str) -> str:
    now = datetime.utcnow()
    safe_city = re.sub(r"[^a-zA-Z0-9_-]", "_", city)
    return f"{_today_prefix()}{safe_city}_{now.hour:02d}{now.minute:02d}{now.second:02d}.json"


def _get_latest_cached(s3_client, bucket: str, city: str) -> dict | None:
    """Look for the most recent S3 object under today's prefix matching city_*.json."""
    prefix = _today_prefix()
    safe_city = re.sub(r"[^a-zA-Z0-9_-]", "_", city)
    pattern = re.compile(re.escape(safe_city) + r"_\d{6}\.json$")

    try:
        paginator = s3_client.get_paginator("list_objects_v2")
        objects = []
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                key = obj.get("Key", "")
                if pattern.search(key):
                    objects.append(obj)

        if not objects:
            return None

        # Sort by LastModified descending, take most recent
        objects.sort(key=lambda o: o.get("LastModified", datetime.min), reverse=True)
        latest = objects[0]
        key = latest["Key"]
        last_modified = latest.get("LastModified")

        # Check freshness
        ttl = _get_cache_ttl()
        if last_modified:
            age = (datetime.utcnow() - last_modified.replace(tzinfo=None)).total_seconds()
            if age > ttl:
                return None

        # Fetch object content
        resp = s3_client.get_object(Bucket=bucket, Key=key)
        body = resp["Body"].read().decode("utf-8")
        return json.loads(body)
    except Exception as e:
        print(f"S3 list/get error: {e}")
        return None


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
    """Normalize OpenWeather API response to our schema (matches weather_to_s3 convention)."""
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


def _write_to_s3(s3_client, bucket: str, city: str, data: dict) -> None:
    """Write weather snapshot to S3."""
    key = _s3_key_for_city(city)
    body = json.dumps(data, indent=2)
    s3_client.put_object(Bucket=bucket, Key=key, Body=body, ContentType="application/json")


def handle_weather(city: str, s3_client, bucket: str, api_key: str) -> dict:
    """Handle GET /weather?city=..."""
    if not city or not city.strip():
        return _error("BAD_REQUEST", "Missing or empty city parameter", 400)

    city = city.strip()

    # Try S3 cache first
    cached = _get_latest_cached(s3_client, bucket, city)
    if cached:
        return _success(cached)

    # Fetch from OpenWeather
    try:
        data = _fetch_from_openweather(city, api_key)
    except RuntimeError as e:
        return _error("OPENWEATHER_ERROR", str(e), 502)

    # Write to S3
    try:
        _write_to_s3(s3_client, bucket, city, data)
    except Exception as e:
        print(f"S3 write error (non-fatal): {e}")
        # Still return the data; caching failed but we have it

    return _success(data)


def handle_cities() -> dict:
    """Handle GET /cities - return allowed city list from env."""
    cities_str = os.environ.get("CITIES", "London,Paris,New York")
    cities = [c.strip() for c in cities_str.split(",") if c.strip()]
    return _success(cities)


def handler(event: dict, context: Any) -> dict:
    """Main Lambda handler. Routes by path and method."""
    http_method = event.get("httpMethod", "GET")
    path = (event.get("path") or "/").rstrip("/") or "/"
    # Normalize path: API Gateway may include stage, e.g. /prod/cities -> /cities
    parts = [p for p in path.split("/") if p]
    if len(parts) >= 2 and parts[0] in ("prod", "dev", "stage", "v1"):
        path = "/" + "/".join(parts[1:])
    elif len(parts) == 1:
        path = "/" + parts[0]
    query_params = event.get("queryStringParameters") or {}

    bucket = _get_env("S3_BUCKET_NAME", "weather-data-bucket-2026")
    api_key = _get_env("OPENWEATHER_API_KEY")
    s3_client = boto3.client("s3")

    if path == "/cities" and http_method == "GET":
        return handle_cities()

    if path == "/weather" and http_method == "GET":
        city = query_params.get("city", "")
        return handle_weather(city, s3_client, bucket, api_key)

    return _error("NOT_FOUND", f"Unknown path: {path}", 404)
