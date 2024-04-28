from tests.initializer import (
    Flight,
    Scheduled,
    TestInitializer,
    create_flights_with_tickets,
    isostring_to_milliseconds,
    milliseconds_to_iso,
    update_scheduled_flights,
)


class TestUpdateFlightsCronjob(TestInitializer):
    __title__ = "Update flights cronjob"

    def test_update_flights_cronjob_successful(self):
        flight_arrival = "2024-04-27T12:29:00.000"
        flight_departure = "2024-04-27T15:15:00.000"

        create_flights_with_tickets(
            tickets=0,
            additional_flight_data={
                "arrival": isostring_to_milliseconds(flight_arrival),
                "departure": isostring_to_milliseconds(flight_departure),
            },
        )

        create_flights_with_tickets(
            tickets=0,
            additional_flight_data={
                "arrival": isostring_to_milliseconds(flight_arrival),
                "departure": isostring_to_milliseconds(flight_departure),
                "scheduled": Scheduled.WEEKLY,
            },
        )

        create_flights_with_tickets(
            tickets=0,
            additional_flight_data={
                "arrival": isostring_to_milliseconds(flight_arrival),
                "departure": isostring_to_milliseconds(flight_departure),
                "scheduled": Scheduled.MONTHLY,
            },
        )

        update_scheduled_flights()

        updated_daily_flight = Flight.find_one({"scheduled": Scheduled.DAILY})
        updated_weekly_flight = Flight.find_one({"scheduled": Scheduled.WEEKLY})
        updated_monthly_flight = Flight.find_one({"scheduled": Scheduled.MONTHLY})

        updated_daily_arrival = milliseconds_to_iso(updated_daily_flight.arrival)
        updated_daily_departure = milliseconds_to_iso(updated_daily_flight.departure)
        self.assertEqual(updated_daily_arrival, "2024-04-28T12:29:00")
        self.assertEqual(updated_daily_departure, "2024-04-28T15:15:00")

        updated_weekly_arrival = milliseconds_to_iso(updated_weekly_flight.arrival)
        updated_weekly_departure = milliseconds_to_iso(updated_weekly_flight.departure)
        self.assertEqual(updated_weekly_arrival, "2024-05-04T12:29:00")
        self.assertEqual(updated_weekly_departure, "2024-05-04T15:15:00")

        updated_monthly_arrival = milliseconds_to_iso(updated_monthly_flight.arrival)
        updated_monthly_departure = milliseconds_to_iso(
            updated_monthly_flight.departure
        )
        self.assertEqual(updated_monthly_arrival, "2024-05-27T12:29:00")
        self.assertEqual(updated_monthly_departure, "2024-05-27T15:15:00")
