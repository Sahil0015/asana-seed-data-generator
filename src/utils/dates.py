"""
Date and time utilities for data generation.
"""
import random
from datetime import datetime, timedelta


def random_date(start_days_ago=180, end_days_ago=0):
    """
    Generate random date within range.
    Returns ISO string format for SQLite compatibility.
    """
    days_ago = random.randint(end_days_ago, start_days_ago)
    dt = datetime.now() - timedelta(days=days_ago)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def now_str():
    """Get current datetime as string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_datetime(dt_str):
    """Parse datetime string back to datetime object."""
    return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")


def add_days(dt_str, days):
    """Add days to a datetime string and return new string."""
    dt = parse_datetime(dt_str)
    new_dt = dt + timedelta(days=days)
    return new_dt.strftime("%Y-%m-%d %H:%M:%S")


def add_hours(dt_str, hours):
    """Add hours to a datetime string and return new string."""
    dt = parse_datetime(dt_str)
    new_dt = dt + timedelta(hours=hours)
    return new_dt.strftime("%Y-%m-%d %H:%M:%S")


def to_date_only(dt_str):
    """Convert datetime string to date-only string."""
    dt = parse_datetime(dt_str)
    return dt.strftime("%Y-%m-%d")
