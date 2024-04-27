import random
import time
from datetime import datetime


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
