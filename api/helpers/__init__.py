import time
from uuid import uuid4


def get_uuid():
    return uuid4().hex


def current_milli_time():
    return round(time.time() * 1000)
