import json
import unittest
from datetime import timedelta

from colorama import Fore

from api.bcrypt_flask import FlaskBcrypt
from api.constants import (
    TEST_QRCODE,
    TICKET_CHILD_DISCOUNT,
    CabinClass,
    Environment,
    Scheduled,
    TicketType,
)
from api.helpers import (
    current_milli_time,
    isostring_to_milliseconds,
    milliseconds_to_iso,
)
from api.main import db, flask_app
from api.models import Admin, Flight, Review, Seat, Ticket, TokenBlocklist, User
from config import DefaultConfig, JWTConfig
from tests.only_meta import OnlyMeta

app = flask_app.app.test_client()
bcrypt = FlaskBcrypt()

from api.helpers.cronjobs import create_default_data
from api.helpers.flights import update_scheduled_flights


class TestInitializer(unittest.TestCase, metaclass=OnlyMeta):
    __title__ = None

    @classmethod
    def setUpClass(cls):
        if DefaultConfig.ENV != Environment.TEST:
            return cls.skipTest(cls, "Please set ENV to test (env ENV=test)")

        cls.__display_title()
        flask_app.app_context.push()

    @classmethod
    def tearDownClass(cls):
        flask_app.app_context.pop()

    @classmethod
    def __display_title(cls):
        if cls.__title__:
            print(f"\n{Fore.CYAN}{cls.__title__} {Fore.WHITE}")

    def setUp(self):
        db.drop_all()
        db.create_all()
        create_default_data()


class UsersConfig:
    def __init__(self):
        self.user_password = "user1234"
        self.admin_password = "admin1234"

    def get_admin(self):
        admin = {
            "email": "admin@gmail.com",
            "password": bcrypt.hash_password(self.admin_password),
        }

        return admin

    def get_user(self):
        user = {
            "email": "user@gmail.com",
            "password": bcrypt.hash_password(self.user_password),
            "name": "User",
            "photo": None,
        }

        return user


user_config = UsersConfig()


class ParsedResponse:
    @property
    def error(self):
        return self.__parsed_response.get("error")

    @property
    def data(self):
        return self.__parsed_response.get("data")

    @property
    def message(self):
        return self.__parsed_response.get("message")

    def __init__(self, response):
        self.__parsed_response = json.loads(response.data)


def get_initial_headers(isAdmin=None):
    headers = {
        "app_token": DefaultConfig.APP_TOKEN,
    }

    if isAdmin:
        headers.update({"referrer-type": "admin"})

    return headers


def create_user(isAdmin=None, **kwargs):
    if isAdmin:
        user = Admin.create(**user_config.get_admin(), **kwargs)
        user.initial_password = user_config.admin_password
    else:
        user = User.create(**user_config.get_user(), **kwargs)
        user.initial_password = user_config.user_password

    return user


def login(user, isAdmin=None):
    login_params = {"email": user.email, "password": user.initial_password}

    headers = get_initial_headers(isAdmin=isAdmin)
    response = app.post("/login", json=login_params, headers=headers)

    parsed_response = ParsedResponse(response)

    if parsed_response.error == 1:
        raise Exception(parsed_response.data)

    return parsed_response.data["access_token"]


def logout(headers, access_token=None):
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    app.post("/logout", headers=headers)


def get_access_token(created_user=None, isAdmin=None, **kwargs):
    user = created_user if created_user else create_user(isAdmin, **kwargs)
    access_token = login(user=user, isAdmin=isAdmin)

    return {"user_id": user.id, "access_token": access_token}


def get_headers(created_access_token=None, isAdmin=None, **kwargs):
    res = (
        created_access_token
        if created_access_token
        else get_access_token(isAdmin=isAdmin, **kwargs)
    )

    access_token = res["access_token"]
    user_id = res["user_id"]

    headers = {"Authorization": f"Bearer {access_token}", "user_id": user_id}
    initial_headers = get_initial_headers(isAdmin=isAdmin)

    headers.update(initial_headers)

    return headers


def get_second_headers():
    password = "second123"
    hashed_password = bcrypt.hash_password(password)

    new_user = User.create(
        email="seconduser@gmail.com", password=hashed_password, name="seconduser"
    )
    new_user.initial_password = password

    access_token = login(user=new_user)
    headers = get_headers(created_access_token=access_token)
    return headers


def create_flights_with_tickets(user_id=None, additional_flight_data={}, tickets=1):
    flight_data = {
        "airline": "United",
        "cabin_class": CabinClass.FIRST,
        "departure": current_milli_time(),
        "arrival": current_milli_time() + 1000,
        "latitude": 34.0573868,
        "longitude": -118.3535625,
        "score": 8.5,
        "scheduled": Scheduled.DAILY,
        "price": 150,
        "currency": "€",
        **additional_flight_data,
    }

    flight = Flight.create(**flight_data)
    if not user_id:
        return flight

    seats = Seat.find({"cabin_class": flight.cabin_class})

    for index in range(tickets):
        seat = seats[index]

        ticket_data = {
            "user_id": user_id,
            "flight_id": flight.id,
            "seat_id": seat.id,
            "price": 150,
            "currency": "€",
            "name": "User",
            "surname": "Test",
            "date_of_birth": current_milli_time(),
            "qrcode": TEST_QRCODE,
        }

        Ticket.create(**ticket_data)

    return flight


__all__ = [
    timedelta,
    JWTConfig,
    TokenBlocklist,
    Review,
    Flight,
    CabinClass,
    Scheduled,
    Ticket,
    Seat,
    TicketType,
    TEST_QRCODE,
    TICKET_CHILD_DISCOUNT,
    isostring_to_milliseconds,
    update_scheduled_flights,
    milliseconds_to_iso,
]
