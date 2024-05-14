from tests.initializer import (
    Flight,
    ParsedResponse,
    TestInitializer,
    app,
    create_flights_with_tickets,
    current_milli_time,
    get_headers,
    get_initial_headers,
    logout,
)


class TestGetFlight(TestInitializer):
    __title__ = "GET /flight"

    def test_get_flight_with_taken_seats_successful(self):
        headers = get_headers()
        user_id = headers.get("user_id")

        tickets_to_create = 3
        created_fligth = create_flights_with_tickets(
            user_id=user_id, tickets=tickets_to_create
        )

        response = app.get(f"/flight?flight_id={created_fligth.id}", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        flight = parsed_response.data

        self.assertEqual(flight.get("airline"), created_fligth.airline)
        self.assertEqual(flight.get("cabin_class"), created_fligth.cabin_class)
        self.assertEqual(flight.get("departure"), created_fligth.departure)
        self.assertEqual(flight.get("arrival"), created_fligth.arrival)
        self.assertEqual(flight.get("from_latitude"), created_fligth.from_latitude)
        self.assertEqual(flight.get("from_longitude"), created_fligth.from_longitude)
        self.assertEqual(flight.get("to_latitude"), created_fligth.to_latitude)
        self.assertEqual(flight.get("to_longitude"), created_fligth.to_longitude)
        self.assertEqual(flight.get("score"), created_fligth.score)
        self.assertEqual(flight.get("scheduled"), created_fligth.scheduled)
        self.assertEqual(flight.get("price"), created_fligth.price)
        self.assertEqual(flight.get("currency"), created_fligth.currency)

        self.assertEqual(flight.get("id"), created_fligth.id)

        self.assertIsInstance(flight.get("created_at"), int)
        self.assertIsInstance(flight.get("updated_at"), int)

        available_seats = flight.get("available_seats")
        seats = flight.get("seats")

        self.assertEqual(len(available_seats), len(seats) - tickets_to_create)

        logout(headers)

    def test_get_flight_without_taken_seats_successful(self):
        headers = get_headers()
        user_id = headers.get("user_id")

        created_fligth = create_flights_with_tickets(user_id=user_id, tickets=0)

        response = app.get(f"/flight?flight_id={created_fligth.id}", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        flight = parsed_response.data

        self.assertEqual(flight.get("id"), created_fligth.id)

        available_seats = flight.get("available_seats")
        seats = flight.get("seats")

        self.assertEqual(len(available_seats), len(seats))

        logout(headers)

    def test_get_no_flight_successful(self):
        headers = get_initial_headers()

        response = app.get(
            "/flight?flight_id=c6a3e4095cd5423db8eb83e5de7266dd", headers=headers
        )
        parsed_response = ParsedResponse(response)
        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        self.assertIsNone(parsed_response.data)

    def test_cannot_get_expired_flight(self):
        headers = get_headers()
        user_id = headers.get("user_id")

        created_fligth = create_flights_with_tickets(
            user_id=user_id,
            tickets=0,
            additional_flight_data={"arrival": current_milli_time() - 1000},
        )

        response = app.get(f"/flight?flight_id={created_fligth.id}", headers=headers)
        parsed_response = ParsedResponse(response)
        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        self.assertIsNone(parsed_response.data)

        logout(headers)

    def test_cannot_get_deleted_flight(self):
        headers = get_headers()
        user_id = headers.get("user_id")

        created_fligth = create_flights_with_tickets(
            user_id=user_id,
            tickets=0,
        )

        Flight.update_one(created_fligth.id, is_deleted=True)

        response = app.get(f"/flight?flight_id={created_fligth.id}", headers=headers)
        parsed_response = ParsedResponse(response)
        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        self.assertIsNone(parsed_response.data)

        logout(headers)

    def test_passing_wrong_params(self):
        headers = get_initial_headers()
        response = app.get("/flight?flight_id=", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        [flightIdError] = parsed_response.data.get("flight_id")

        self.assertEqual(flightIdError, "Not a valid UUID.")

    def test_passing_empty_params(self):
        headers = get_initial_headers()
        response = app.get("/flight", headers=headers)
        parsed_response = ParsedResponse(response)

        missing_data_error = "Missing data for required field."

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        [flightIdError] = parsed_response.data.get("flight_id")

        self.assertEqual(flightIdError, missing_data_error)

    def test_passing_empty_headers(self):
        response = app.get("/flight", headers={})
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "app-token is not specified in headers")
