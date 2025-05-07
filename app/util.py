from datetime import datetime, timezone

def str_to_datetime(timestamp_str: str) -> datetime:
    """Convert a timestamp to a python datetime object"""
    return datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)