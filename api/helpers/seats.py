from api.constants import SEATS_DATA, Environment
from api.models import Seat
from config import DefaultConfig


def create_default_seats():
    try:
        seats = Seat.find()
        if len(seats) > 0:
            return

        for seat in SEATS_DATA:
            created_seat = Seat.create(**seat)

            if DefaultConfig.ENV != Environment.TEST:
                print(f"{created_seat} was created successfully")
    except Exception as e:
        print(f"ERROR (create_default_seats): {e}")
