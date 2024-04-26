from api.helpers import current_milli_time
from api.models import Flight, Seat, Ticket


def get_available_seats(flight: Flight):
    try:
        seats = Seat.find({"cabin_class": flight.cabin_class})

        tickets = Ticket.find(
            join=[
                {"table": Seat, "condition": Ticket.seat_id == Seat.id},
                {
                    "table": Flight,
                    "condition": Ticket.flight_id == Flight.id,
                },
            ],
            comparative_condition=[
                Flight.arrival >= current_milli_time(),
                Seat.cabin_class == Flight.cabin_class,
                Flight.id == flight.id,
            ],
        )
    except Exception as e:
        print(f"ERROR (get_available_seats): {e}")

    taken_seats = []
    for ticket in tickets:
        taken_seats.append(ticket.seat)

    available_seats = [seat.serialize() for seat in seats if seat not in taken_seats]

    return available_seats
