"""Functions for working with dates."""

from datetime import datetime


def convert_to_datetime(date: str) -> datetime:
    """Takes a string and returns a datetime"""
    try:
        return datetime.strptime(date, "%d.%m.%Y")
    except ValueError:
        raise ValueError("Unable to convert value to datetime.")


def get_days_between(first: datetime, last: datetime) -> int:
    """Finds the difference between two datetimes and returns as an integer"""
    if not (isinstance(first, datetime) and isinstance(last, datetime)):
        raise TypeError("Datetimes required.")
    return (last-first).days


def get_day_of_week_on(date: datetime) -> str:
    """Takes a datetime and return the day of the week it occurs on"""
    if not isinstance(date, datetime):
        raise TypeError("Datetime required.")
    return datetime.strftime(date, "%A")
