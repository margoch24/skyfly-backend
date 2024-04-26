from flask_jwt_extended import get_jwt_identity

from api.helpers import current_milli_time
from api.helpers.flights import get_available_seats
from api.helpers.models import prepare_condition
from api.models import Admin, Flight


class FlightsService:

    def get_flights(
        arrival: int,
        cabin_class: str,
        departure: int,
        latitude: float,
        longitude: float,
        page: int,
        price: float,
        limit: int,
    ):
        return get_flights(
            arrival, cabin_class, departure, latitude, longitude, page, price, limit
        )

    def get_flight(flight_id):
        return get_flight(flight_id)

    def create_flight(
        arrival: str,
        airline: str,
        cabin_class: str,
        departure: str,
        latitude: float,
        longitude: float,
        photo: str,
        score: float,
        scheduled: str,
        price: float,
        currency: str,
    ):
        return create_flight(
            arrival,
            airline,
            cabin_class,
            departure,
            latitude,
            longitude,
            photo,
            score,
            scheduled,
            price,
            currency,
        )


def get_flights(
    arrival: int,
    cabin_class: str,
    departure: int,
    latitude: float,
    longitude: float,
    page: int,
    price: float,
    limit: int,
):
    serialized_flights = []

    try:
        config = {
            "arrival": {"type": "datetime"},
            "departure": {"type": "datetime"},
            "price": {"type": "range"},
            "cabin_class": {"type": "in"},
        }
        [comparative_condition, condition] = prepare_condition(
            cls=Flight,
            config=config,
            arrival=arrival,
            cabin_class=cabin_class,
            departure=departure,
            latitude=latitude,
            longitude=longitude,
            price=price,
        )

        flights = Flight.find(
            order_by=[Flight.created_at.desc()],
            page=page,
            comparative_condition=[
                *comparative_condition,
                Flight.arrival >= current_milli_time(),
            ],
            condition=condition,
            limit=limit,
        )

        for flight in flights:
            available_seats_amount = len(get_available_seats(flight))
            flight_with_seats = {
                **flight.serialize(),
                "available_seats": available_seats_amount,
            }
            serialized_flights.append(flight_with_seats)
    except Exception as e:
        print(f"ERROR (get_flights): {e}")

        response = {"error": 1, "data": {"message": "Internal server error"}}
        return response, 500

    response = {
        "error": 0,
        "data": serialized_flights,
    }
    return response, 200


def get_flight(flight_id):
    try:
        flight = Flight.find_one(
            condition={"id": flight_id, "is_deleted": False},
            comparative_condition=[Flight.arrival >= current_milli_time()],
        )
    except Exception as e:
        print(f"ERROR (get_flight): {e}")

        response = {"error": 1, "data": {"message": "Internal server error"}}
        return response, 500

    if not flight:
        response = {
            "error": 0,
            "data": None,
        }
        return response, 200

    response = {
        "error": 0,
        "data": {**flight.serialize(), "available_seats": get_available_seats(flight)},
    }
    return response, 200


def create_flight(
    arrival: str,
    airline: str,
    cabin_class: str,
    departure: str,
    latitude: float,
    longitude: float,
    photo: str,
    score: float,
    scheduled: str,
    price: float,
    currency: str,
):
    try:
        admin_id = get_jwt_identity()
        admin_exist = Admin.find_one({"id": admin_id, "is_deleted": False})

        if not admin_exist:
            response = {"error": 1, "data": {"message": "Insufficient permissions"}}
            return response, 403

        flight = Flight.create(
            arrival=arrival,
            airline=airline,
            cabin_class=cabin_class,
            departure=departure,
            latitude=latitude,
            longitude=longitude,
            photo=photo,
            score=score,
            scheduled=scheduled,
            price=price,
            currency=currency,
        )
    except Exception as e:
        print(f"ERROR (create_flight): {e}")

    if not flight:
        response = {"error": 1, "data": {"message": "Internal server error"}}
        return response, 500

    response = {
        "error": 0,
        "data": flight.serialize(),
    }
    return response, 200
