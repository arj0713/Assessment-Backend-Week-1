"""Functions for working with dates."""

from datetime import datetime


def convert_to_datetime(date: str) -> datetime:
    if not isinstance(date, str):
        raise TypeError("Input must be a string")
    try:
        date = datetime.strptime(date, "%d.%m.%Y")
    except ValueError:
        raise ValueError("Unable to convert value to datetime.")
    return date


def get_days_between(first: datetime, last: datetime) -> int:
    if not (isinstance(first, datetime) and isinstance(last, datetime)):
        raise TypeError("Datetimes required.")
    return (last-first).days


def get_day_of_week_on(date: datetime) -> str:
    pass
