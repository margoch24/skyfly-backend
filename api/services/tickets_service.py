from flask_jwt_extended import get_jwt_identity

from api.helpers import current_milli_time
from api.helpers.flights import check_seat_availability
from api.helpers.tickets import calculate_discount, generate_qrcode
from api.models import Flight, Seat, Ticket, User


class TicketsService:

    def create_ticket(
        name: str, surname: str, date_of_birth: int, flight_id: str, seat_id: str
    ):
        return create_ticket(name, surname, date_of_birth, flight_id, seat_id)

    def get_tickets(limit: int, page: int, type: str):
        return get_tickets(limit, page, type)


def get_tickets(limit: int, page: int, type: str):
    try:
        user_id = get_jwt_identity()

        user_exist = User.find_one({"id": user_id, "is_deleted": False})
        if not user_exist:
            response = {"error": 1, "data": {"message": "Insufficient permissions"}}
            return response, 403

        comparative_condition = [
            Seat.cabin_class == Flight.cabin_class,
            Ticket.is_deleted == False,
            Flight.is_deleted == False,
            Ticket.user_id == user_id,
        ]

        if type == "past":
            comparative_condition.append(Flight.arrival < current_milli_time())

        if type == "future":
            comparative_condition.append(Flight.arrival >= current_milli_time())

        tickets = Ticket.find(
            order_by=[Ticket.created_at.desc()],
            page=page,
            limit=limit,
            join=[
                {"table": Seat, "condition": Ticket.seat_id == Seat.id},
                {
                    "table": Flight,
                    "condition": Ticket.flight_id == Flight.id,
                },
            ],
            comparative_condition=comparative_condition,
        )
    except Exception as e:
        print(f"ERROR (get_tickets): {e}")

        response = {"error": 1, "data": {"message": "Internal server error"}}
        return response, 500

    serialized_tickets = [
        {
            **ticket.serialize(),
            "seat": ticket.seat.serialize(),
            "flight": ticket.flight.serialize(),
        }
        for ticket in tickets
    ]

    response = {
        "error": 0,
        "data": serialized_tickets,
    }
    return response, 200


def create_ticket(
    name: str, surname: str, date_of_birth: int, flight_id: str, seat_id: str
):
    try:
        user_id = get_jwt_identity()

        user_exist = User.find_one({"id": user_id, "is_deleted": False})
        if not user_exist:
            response = {"error": 1, "data": {"message": "Insufficient permissions"}}
            return response, 403

        flight_exist = Flight.find_one(
            {"id": flight_id, "is_deleted": False},
            comparative_condition=[
                Flight.arrival >= current_milli_time(),
            ],
        )
        if not flight_exist:
            response = {"error": 1, "data": {"message": "Flight does not exist"}}
            return response, 400

        seat_exist = Seat.find_one({"id": seat_id, "is_deleted": False})
        if not seat_exist:
            response = {"error": 1, "data": {"message": "Seat does not exist"}}
            return response, 400

        is_seat_available = check_seat_availability(
            flight=flight_exist, seat_id=seat_id
        )
        if not is_seat_available:
            response = {"error": 1, "data": {"message": "The seat is already taken"}}
            return response, 400

        [price, ticket_type] = calculate_discount(
            flight=flight_exist, date_of_birth=date_of_birth
        )

        ticket = Ticket.create(
            name=name,
            surname=surname,
            date_of_birth=date_of_birth,
            seat_id=seat_exist.id,
            flight_id=flight_exist.id,
            user_id=user_id,
            currency=flight_exist.currency,
            price=price,
            type=ticket_type,
        )

        qrcode = generate_qrcode(ticket_id=ticket.id)

        updated_ticket = Ticket.update_one(ticket.id, qrcode=qrcode)
    except Exception as e:
        print(f"ERROR (create_ticket): {e}")

    if not ticket or not updated_ticket or not qrcode:
        response = {"error": 1, "data": {"message": "Internal server error"}}
        return response, 500

    response = {
        "error": 0,
        "data": ticket.serialize(),
    }
    return response, 200
