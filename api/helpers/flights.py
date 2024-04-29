from api.constants import Environment, Scheduled
from api.helpers import current_milli_time, days_to_milliseconds
from api.models import Flight, Seat, Ticket
from config import DefaultConfig


def get_available_seats(flight: Flight):
    try:
        found_seats = Seat.find({"cabin_class": flight.cabin_class})

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

    available_seats = [
        seat.serialize() for seat in found_seats if seat not in taken_seats
    ]
    seats = [seat.serialize() for seat in found_seats]

    return available_seats, seats


def check_seat_availability(seat_id, flight):
    available_seats, *_ = get_available_seats(flight=flight)
    for seat in available_seats:
        if seat.get("id") == seat_id:
            return True
    return False


def update_scheduled_flights():
    try:
        if DefaultConfig.ENV != Environment.TEST:
            print("Start the update of scheduled flight")

        flights = Flight.find(
            comparative_condition=[Flight.arrival < current_milli_time()],
        )

        if len(flights) <= 0:
            return

        for flight in flights:
            days_increment = 0

            match flight.scheduled:
                case Scheduled.DAILY:
                    days_increment = 1

                case Scheduled.WEEKLY:
                    days_increment = 7

                case Scheduled.MONTHLY:
                    days_increment = 30

            milli_days_increment = days_to_milliseconds(days_increment)
            new_arrival = flight.arrival + milli_days_increment
            new_departure = flight.departure + milli_days_increment

            updated_flight = flight.update_one(
                flight.id, arrival=new_arrival, departure=new_departure
            )

            if DefaultConfig.ENV != Environment.TEST:
                print(f"{updated_flight} was updated successfully")
    except Exception as e:
        print(f"ERROR (update_scheduled_flights): {e}")

    finally:
        if DefaultConfig.ENV != Environment.TEST:
            print("End the update of scheduled flight")
