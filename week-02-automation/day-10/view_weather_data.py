"""view_weather_data.py
Utility script to browse and inspect weather JSON objects stored in S3 by the weather_to_s3.py pipeline.

Features:
- List recent objects for a given date and/or city
- Download and pretty-print JSON for selected objects
- Filter by date prefix (YYYY-MM-DD) and city name

AWS credentials are resolved via the default AWS credential chain.

Configuration:
- S3_BUCKET_NAME (required, same as in weather_to_s3.py)
"""

from __future__ import annotations
import argparse
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv


def setup_logging() -> None:
    """Configure basic console logging with timestamps."""
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
    """Build an S3 client using the default AWS credential chain."""
    return boto3.client("s3")


def build_prefix_for_date_and_city(
    date_str: Optional[str], city: Optional[str],
) -> str:
    """Build an S3 prefix based on optional date and city filter.
    - date_str format: YYYY-MM-DD
    - stored layout: YYYY/MM/DD/city_HHMMSS.json"""
    prefix_parts: List[str] = []
    if date_str:
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError(f"Invalid date format '{date_str}', expected YYYY-MM-DD") from exc
        prefix_parts.append(dt.strftime("%Y/%m/%d"))
    if city:
        city_normalized = city.strip().replace(" ", "_").lower()
        prefix_parts.append(f"{city_normalized}_")
    if not prefix_parts:
        return ""
    return "/".join(prefix_parts)


def list_objects(
    client, bucket: str, prefix: str, max_items: int,
) -> List[Dict[str, Any]]:
    """List up to max_items objects under the given prefix."""
    results: List[Dict[str, Any]] = []
    kwargs = {"Bucket": bucket, "Prefix": prefix} if prefix else {"Bucket": bucket}
    while True:
        try:
            resp = client.list_objects_v2(**kwargs)
        except (ClientError, BotoCoreError) as exc:
            logging.error("Failed to list objects from s3://%s/%s: %s", bucket, prefix, exc)
            break
        contents = resp.get("Contents", [])
        for obj in contents:
            results.append(obj)
            if len(results) >= max_items:
                return results
        if not resp.get("IsTruncated"):
            break
        kwargs["ContinuationToken"] = resp.get("NextContinuationToken")
    return results


def fetch_object_json(client, bucket: str, key: str) -> Dict[str, Any]:
    """Download a JSON object from S3 and parse it."""
    try:
        resp = client.get_object(Bucket=bucket, Key=key)
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(f"Failed to download s3://{bucket}/{key}: {exc}") from exc
    body = resp["Body"].read()
    try:
        return json.loads(body.decode("utf-8"))
    except ValueError as exc:
        raise RuntimeError(f"Failed to decode JSON for s3://{bucket}/{key}: {exc}") from exc


def print_summary_table(objs: List[Dict[str, Any]]) -> None:
    """Print a compact summary table (key, size, last modified)."""
    if not objs:
        logging.info("No objects found for the given filters.")
        return
    print(f"{'Index':<5} {'Size(B)':>10} {'LastModified':>25} Key")
    print("-" * 80)
    for idx, obj in enumerate(objs):
        size = obj.get("Size", 0)
        lm = obj.get("LastModified")
        lm_str = lm.isoformat() if hasattr(lm, "isoformat") else str(lm)
        print(f"{idx:<5} {size:>10} {lm_str:>25} {obj.get('Key','')}")


def main() -> int:
    """CLI entrypoint.
    Example usages:
      python view_weather_data.py --date 2026-02-18 --limit 10
      python view_weather_data.py --city London --raw --limit 1"""
    setup_logging()
    parser = argparse.ArgumentParser(description="View weather data stored in S3.")
    parser.add_argument(
        "--date", help="Filter by date (YYYY-MM-DD). Maps to prefixes like YYYY/MM/DD/.",
    )
    parser.add_argument(
        "--city", help="Filter by city name (case-insensitive; spaces -> underscore).",
    )
    parser.add_argument(
        "--limit", type=int, default=20, help="Maximum number of objects to list (default: 20).",
    )
    parser.add_argument(
        "--raw", action="store_true", help="Download and pretty-print JSON for the first matching object.",
    )
    args = parser.parse_args()

    try:
        bucket = load_env_bucket()
    except Exception as exc:
        logging.error("Configuration error: %s", exc)
        return 1

    client = build_s3_client()
    prefix = build_prefix_for_date_and_city(args.date, args.city)
    logging.info("Listing objects in bucket='%s' with prefix='%s'", bucket, prefix or "<root>")
    objects = list_objects(client, bucket, prefix, max_items=args.limit)
    print_summary_table(objects)

    if args.raw and objects:
        key = objects[0]["Key"]
        logging.info("Downloading first object: s3://%s/%s", bucket, key)
        try:
            data = fetch_object_json(client, bucket, key)
        except Exception as exc:
            logging.error("Failed to load JSON from s3://%s/%s: %s", bucket, key, exc)
            return 1
        print(" --- JSON content (first object) ---")
        print(json.dumps(data, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
