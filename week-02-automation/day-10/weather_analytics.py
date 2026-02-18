"""weather_analytics.py
Analytics utility for weather JSON data stored in S3 by weather_to_s3.py.

Features:
- Scan a date range (prefix-based) and optional city filter
- Aggregate per-city statistics (count, min/avg/max temperature)
- Print summary table to the console

AWS credentials are resolved via the default AWS credential chain.
Configuration:
- S3_BUCKET_NAME (required, same as in weather_to_s3.py)
"""

from __future__ import annotations
import argparse
import json
import logging
import os
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, Iterable, List, Optional
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv


def setup_logging() -> None:
    """Configure console logging with timestamps."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def load_env_bucket() -> str:
    """Load S3 bucket name from environment (.env). Required: S3_BUCKET_NAME"""
    load_dotenv()
    bucket = os.getenv("S3_BUCKET_NAME")
    if not bucket:
        raise RuntimeError("S3_BUCKET_NAME must be set in environment/.env")

return bucket


def build_s3_client():
    """Build an S3 client using the default credential chain."""
    return boto3.client("s3")


def date_range(start: datetime, end: datetime) -> Iterable[datetime]:
    """Inclusive date range generator (day by day)."""
    cur = start
    while cur <= end:
        yield cur
        cur += timedelta(days=1)


def prefix_for_date(dt: datetime) -> str:
    """Convert a date into the S3 prefix used by weather_to_s3.py. Example: 2026-02-18 -> "2026/02/18/" """
    return dt.strftime("%Y/%m/%d/")


def normalize_city_for_filter(city: Optional[str]) -> Optional[str]:
    """Normalize user-provided city name for filtering. Example: "New York" -> "new_york" """
    if not city:
        return None
    return city.strip().replace(" ", "_").lower()


def list_objects_for_prefix(client, bucket: str, prefix: str) -> List[Dict[str, Any]]:
    """List all objects for a single prefix."""
    results: List[Dict[str, Any]] = []
    kwargs = {"Bucket": bucket, "Prefix": prefix}
    while True:
        try:
            resp = client.list_objects_v2(**kwargs)
        except (ClientError, BotoCoreError) as exc:
            logging.error("Failed to list objects from s3://%s/%s: %s", bucket, prefix, exc)
            break
        contents = resp.get("Contents", [])
        results.extend(contents)
        if not resp.get("IsTruncated"):
            break
        kwargs["ContinuationToken"] = resp.get("NextContinuationToken")
    return results


def fetch_json(client, bucket: str, key: str) -> Optional[Dict[str, Any]]:
    """Download an S3 JSON object and parse it. Returns None if download or parsing fails."""
    try:
        resp = client.get_object(Bucket=bucket, Key=key)
        data = resp["Body"].read()
        return json.loads(data.decode("utf-8"))
    except (ClientError, BotoCoreError, ValueError) as exc:
        logging.error("Failed to load JSON from s3://%s/%s: %s", bucket, key, exc)
        return None


@dataclass
class CityStats:
    """Accumulated statistics for a single city."""
    count: int = 0
    temp_sum: float = 0.0
    temp_min: Optional[float] = None
    temp_max: Optional[float] = None


def update_stats(stats: CityStats, temp_c: float) -> None:
    """Update CityStats with a new temperature value."""
    stats.count += 1
    stats.temp_sum += temp_c
    if stats.temp_min is None or temp_c < stats.temp_min:
        stats.temp_min = temp_c
    if stats.temp_max is None or temp_c > stats.temp_max:
        stats.temp_max = temp_c


def print_city_stats_table(city_stats: Dict[str, CityStats]) -> None:
    """Print a table summarizing per-city statistics."""
    if not city_stats:
        logging.info("No data points matched the requested filters.")
        return

    header = f"{'City':<20} {'Count':>8} {'MinTemp(C)':>12} {'AvgTemp(C)':>12} {'MaxTemp(C)':>12}"
    print(header)
    print("-" * len(header))
    for city, stats in sorted(city_stats.items()):
        avg = stats.temp_sum / stats.count if stats.count else 0.0
        min_temp = stats.temp_min if stats.temp_min is not None else float("nan")
        max_temp = stats.temp_max if stats.temp_max is not None else float("nan")
        print(f"{city:<20} {stats.count:>8} {min_temp:>12.2f} {avg:>12.2f} {max_temp:>12.2f}")


def main() -> int:
    """CLI entrypoint."""
    setup_logging()
    parser = argparse.ArgumentParser(description="Run analytics over weather data stored in S3.")
    parser.add_argument("--date", help="Analyze a single date (YYYY-MM-DD).")
    parser.add_argument("--start-date", help="Start date (YYYY-MM-DD) for range analysis.")
    parser.add_argument("--end-date", help="End date (YYYY-MM-DD) for range analysis.")
    parser.add_argument("--city", help="Optional city filter (case-insensitive)")
    args = parser.parse_args()

    if args.date and (args.start_date or args.end_date):
        logging.error("--date cannot be combined with --start-date/--end-date")
        return 1

    try:
        bucket = load_env_bucket()
    except Exception as exc:
        logging.error("Configuration error: %s", exc)
        return 1

    try:
        if args.date:
            start = end = datetime.strptime(args.date, "%Y-%m-%d")
        else:
            if not args.start_date or not args.end_date:
                logging.error("Either --date OR both --start-date and --end-date must be provided.")
                return 1
            start = datetime.strptime(args.start_date, "%Y-%m-%d")
            end = datetime.strptime(args.end_date, "%Y-%m-%d")
    except ValueError as exc:
        logging.error("Invalid date format: %s", exc)
        return 1

    city_filter = normalize_city_for_filter(args.city)
    client = build_s3_client()
    city_stats: Dict[str, CityStats] = defaultdict(CityStats)

    for dt in date_range(start, end):
        prefix = prefix_for_date(dt)
        logging.info("Scanning s3://%s/%s", bucket, prefix)
        objs = list_objects_for_prefix(client, bucket, prefix)
        for obj in objs:
            key = obj["Key"]
            if city_filter:
                filename = key.rsplit("/", 1)[-1]
                city_part = filename.split("_", 1)[0]
                if city_part.lower() != city_filter:
                    continue
            doc = fetch_json(client, bucket, key)
            if not doc:
                continue
            temp = doc.get("temperature_c")
            city_name = str(doc.get("city") or "unknown")
            if not isinstance(temp, (int, float)):
                continue
            update_stats(city_stats[city_name], float(temp))

    print_city_stats_table(city_stats)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
