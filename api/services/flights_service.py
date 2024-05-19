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
        page: int,
        price: float,
        limit: int,
        from_latitude: float,
        from_longitude: float,
        to_latitude: float,
        to_longitude: float,
    ):
        return get_flights(
            arrival,
            cabin_class,
            departure,
            page,
            price,
            limit,
            from_latitude,
            from_longitude,
            to_latitude,
            to_longitude,
        )

    def get_flight(flight_id):
        return get_flight(flight_id)

    def create_flight(
        arrival: str,
        airline: str,
        cabin_class: str,
        departure: str,
        photo: str,
        score: float,
        scheduled: str,
        price: float,
        currency: str,
        from_latitude: float,
        from_longitude: float,
        to_latitude: float,
        to_longitude: float,
    ):
        return create_flight(
            arrival,
            airline,
            cabin_class,
            departure,
            photo,
            score,
            scheduled,
            price,
            currency,
            from_latitude,
            from_longitude,
            to_latitude,
            to_longitude,
        )


def get_flights(
    arrival: int,
    cabin_class: str,
    departure: int,
    page: int,
    price: float,
    limit: int,
    from_latitude: float,
    from_longitude: float,
    to_latitude: float,
    to_longitude: float,
):
    serialized_flights = []

    try:
        config = {
            "arrival": {"type": "datetime"},
            "departure": {"type": "datetime"},
            "price": {"type": "range"},
            "cabin_class": {"type": "in"},
        }
        comparative_condition, condition = prepare_condition(
            cls=Flight,
            config=config,
            arrival=arrival,
            cabin_class=cabin_class,
            departure=departure,
            price=price,
            from_latitude=from_latitude,
            from_longitude=from_longitude,
            to_latitude=to_latitude,
            to_longitude=to_longitude,
        )

        flights = Flight.find(
            order_by=[Flight.created_at.desc()],
            page=page,
            comparative_condition=[
                *comparative_condition,
                Flight.departure >= current_milli_time(),
            ],
            condition={**condition, "is_deleted": False},
            limit=limit,
        )

        for flight in flights:
            available_seats, *_ = get_available_seats(flight)
            available_seats_amount = len(available_seats)

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

    available_seats, seats = get_available_seats(flight)

    response = {
        "error": 0,
        "data": {
            **flight.serialize(),
            "available_seats": available_seats,
            "seats": seats,
        },
    }
    return response, 200


def create_flight(
    arrival: str,
    airline: str,
    cabin_class: str,
    departure: str,
    photo: str,
    score: float,
    scheduled: str,
    price: float,
    currency: str,
    from_latitude: float,
    from_longitude: float,
    to_latitude: float,
    to_longitude: float,
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
            from_latitude=from_latitude,
            from_longitude=from_longitude,
            to_latitude=to_latitude,
            to_longitude=to_longitude,
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
