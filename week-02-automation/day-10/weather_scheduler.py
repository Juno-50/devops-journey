"""weather_scheduler.py
Simple scheduler wrapper for weather_to_s3.py.

This script periodically invokes weather_to_s3.py using the same Python interpreter,
relying on the default AWS credential chain and the .env configuration already used
by the main pipeline.

Configuration (via environment/.env):
- WEATHER_FETCH_INTERVAL_SECONDS (optional, default: 900 seconds / 15 minutes)

Usage examples:
  # Run a single immediate pipeline execution (no loop)
  python weather_scheduler.py --once

  # Run pipeline every 15 minutes (or configured interval)
  python weather_scheduler.py
"""

from __future__ import annotations
import argparse
import logging
import os
import subprocess
import sys
import time
from typing import Optional
from dotenv import load_dotenv


def setup_logging() -> None:
    """Configure console logging with timestamps."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def load_interval_seconds(default: int = 900) -> int:
    """
    Load WEATHER_FETCH_INTERVAL_SECONDS from environment.
    If not set or invalid, fall back to the provided default (seconds).
    """
    load_dotenv()
    raw = os.getenv("WEATHER_FETCH_INTERVAL_SECONDS")
    if not raw:
        return default
    try:
        value = int(raw)
        if value <= 0:
            raise ValueError("interval must be positive")
        return value
    except ValueError:
        logging.warning(
            "Invalid WEATHER_FETCH_INTERVAL_SECONDS='%s'; using default %d seconds.",
            raw, default,
        )
        return default


def run_pipeline_once() -> int:
    """
    Invoke weather_to_s3.py as a subprocess using the current Python interpreter.
    Returns the subprocess exit code.
    """
    cmd = [sys.executable, "weather_to_s3.py"]
    logging.info("Executing command: %s", " ".join(cmd))
    try:
        result = subprocess.run(cmd, check=False)
        logging.info("weather_to_s3.py exited with code %d", result.returncode)
        return result.returncode
    except Exception as exc:
        logging.error("Failed to run weather_to_s3.py: %s", exc)
        return 1


def run_scheduler_loop(interval_seconds: int) -> int:
    """
    Run an infinite loop that executes the pipeline and sleeps.
    The loop continues even if individual runs fail; failures are logged.
    Ctrl+C (KeyboardInterrupt) stops the loop.
    """
    logging.info(
        "Starting scheduler loop with interval=%d seconds. Press Ctrl+C to stop.",
        interval_seconds,
    )
    while True:
        exit_code = run_pipeline_once()
        if exit_code == 0:
            logging.info("Pipeline run completed successfully.")
        else:
            logging.warning(
                "Pipeline run completed with non-zero exit code: %d",
                exit_code
            )
        logging.info("Sleeping for %d seconds before next run...", interval_seconds)
        try:
            time.sleep(interval_seconds)
        except KeyboardInterrupt:
            logging.info("Interrupted by user; stopping scheduler loop.")
            return 0


def main() -> int:
    """
    CLI entrypoint. Provides a simple `--once` mode and a long-running scheduler loop.
    """
    setup_logging()
    parser = argparse.ArgumentParser(
        description="Simple scheduler wrapper around weather_to_s3.py."
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run the pipeline only once and exit.",
    )
    args = parser.parse_args()

    if args.once:
        return run_pipeline_once()

    interval = load_interval_seconds()
    return run_scheduler_loop(interval)


if __name__ == "__main__":
    raise SystemExit(main())
