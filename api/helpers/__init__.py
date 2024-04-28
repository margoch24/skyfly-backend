import random
import time
from datetime import datetime, timedelta


def current_milli_time():
    return round(time.time() * 1000)


def get_random(maximum: int):
    random_number = random.random()
    multiplied = random_number * maximum
    return int(multiplied)


def isostring_to_milliseconds(iso_string: str):
    date = datetime.fromisoformat(iso_string)
    milliseconds = int(date.timestamp() * 1000)
    return milliseconds


def days_to_milliseconds(days):
    return timedelta(days=days).total_seconds() * 1000


def milliseconds_to_iso(milliseconds):
    seconds = milliseconds / 1000
    date = datetime.fromtimestamp(seconds)
    iso_string = date.isoformat()
    return iso_string
