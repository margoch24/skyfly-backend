import time

from tests.initializer import (
    TEST_QRCODE,
    TICKET_CHILD_DISCOUNT,
    JWTConfig,
    ParsedResponse,
    Seat,
    TestInitializer,
    Ticket,
    TicketType,
    User,
    app,
    create_flights_with_tickets,
    current_milli_time,
    get_headers,
    get_initial_headers,
    isostring_to_milliseconds,
    logout,
    timedelta,
)


class TestPostTicket(TestInitializer):
    __title__ = "POST /ticket"

    def test_post_ticket_successful(self):
        headers = get_headers()
        user_id = headers.get("user_id")

        flight = create_flights_with_tickets(user_id, tickets=0)
        seat = Seat.find_one({"cabin_class": flight.cabin_class, "column": "B"})

        iso_birth_date = "2000-04-27T16:04:55.000"
        ticket_params = {
            "name": "User",
            "surname": "Test",
            "date_of_birth": isostring_to_milliseconds(iso_birth_date),
            "seat_id": seat.id,
            "flight_id": flight.id,
        }

        response = app.post("/ticket", json=ticket_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        ticket = parsed_response.data

        self.assertEqual(ticket.get("user_id"), headers["user_id"])
        self.assertEqual(ticket.get("name"), ticket_params["name"])
        self.assertEqual(ticket.get("date_of_birth"), ticket_params["date_of_birth"])
        self.assertEqual(ticket.get("date_of_birth"), ticket_params["date_of_birth"])
        self.assertEqual(ticket.get("seat_id"), seat.id)
        self.assertEqual(ticket.get("flight_id"), flight.id)

        self.assertEqual(ticket.get("currency"), flight.currency)
        self.assertEqual(ticket.get("price"), flight.price)
        self.assertEqual(ticket.get("type"), TicketType.ADULT)

        self.assertEqual(ticket.get("qrcode"), TEST_QRCODE)

        self.assertIsNotNone(ticket.get("id"))

        self.assertIsInstance(ticket.get("created_at"), int)
        self.assertIsInstance(ticket.get("updated_at"), int)

        logout(headers)

    def test_post_child_ticket_successful(self):
        headers = get_headers()
        user_id = headers.get("user_id")

        flight = create_flights_with_tickets(user_id, tickets=0)
        seat = Seat.find_one({"cabin_class": flight.cabin_class, "column": "B"})

        iso_birth_date = "2020-04-27T16:04:55.000"
        ticket_params = {
            "name": "User",
            "surname": "Test",
            "date_of_birth": isostring_to_milliseconds(iso_birth_date),
            "seat_id": seat.id,
            "flight_id": flight.id,
        }

        response = app.post("/ticket", json=ticket_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        ticket = parsed_response.data

        self.assertEqual(ticket.get("user_id"), headers["user_id"])
        self.assertEqual(ticket.get("name"), ticket_params["name"])
        self.assertEqual(ticket.get("date_of_birth"), ticket_params["date_of_birth"])
        self.assertEqual(ticket.get("date_of_birth"), ticket_params["date_of_birth"])
        self.assertEqual(ticket.get("seat_id"), seat.id)
        self.assertEqual(ticket.get("flight_id"), flight.id)

        self.assertEqual(ticket.get("currency"), flight.currency)
        self.assertEqual(ticket.get("price"), flight.price * TICKET_CHILD_DISCOUNT)
        self.assertEqual(ticket.get("type"), TicketType.CHILD)

        self.assertEqual(ticket.get("qrcode"), TEST_QRCODE)

        self.assertIsNotNone(ticket.get("id"))

        self.assertIsInstance(ticket.get("created_at"), int)
        self.assertIsInstance(ticket.get("updated_at"), int)

        logout(headers)

    def test_insufficient_permissions(self):
        headers = get_headers()
        user_id = headers.get("user_id")

        User.update_one(user_id, is_deleted=True)

        flight = create_flights_with_tickets(user_id, tickets=0)
        seat = Seat.find_one({"cabin_class": flight.cabin_class, "column": "B"})

        ticket_params = {
            "name": "User",
            "surname": "Test",
            "date_of_birth": current_milli_time(),
            "seat_id": seat.id,
            "flight_id": flight.id,
        }

        response = app.post("/ticket", json=ticket_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "403 FORBIDDEN")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Insufficient permissions")

        logout(headers)

    def test_flight_does_not_exist(self):
        headers = get_headers()

        seat = Seat.find_one()

        ticket_params = {
            "name": "User",
            "surname": "Test",
            "date_of_birth": current_milli_time(),
            "seat_id": seat.id,
            "flight_id": seat.id,
        }

        response = app.post("/ticket", json=ticket_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Flight does not exist")

        logout(headers)

    def test_seat_does_not_exist(self):
        headers = get_headers()
        user_id = headers.get("user_id")

        flight = create_flights_with_tickets(user_id, tickets=0)

        ticket_params = {
            "name": "User",
            "surname": "Test",
            "date_of_birth": current_milli_time(),
            "seat_id": flight.id,
            "flight_id": flight.id,
        }

        response = app.post("/ticket", json=ticket_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Seat does not exist")

        logout(headers)

    def test_seat_is_taken(self):
        headers = get_headers()
        user_id = headers.get("user_id")

        flight = create_flights_with_tickets(user_id, tickets=1)
        created_ticket = Ticket.find_one({"flight_id": flight.id})
        seat = Seat.find_one({"id": created_ticket.seat_id})

        ticket_params = {
            "name": "User",
            "surname": "Test",
            "date_of_birth": current_milli_time(),
            "seat_id": seat.id,
            "flight_id": flight.id,
        }

        response = app.post("/ticket", json=ticket_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "The seat is already taken")

        logout(headers)

    def test_passing_wrong_params(self):
        headers = get_headers()
        ticket_params = {
            "name": True,
            "surname": [],
            "date_of_birth": "string",
            "seat_id": "incorrect uuid",
            "flight_id": 456,
        }

        response = app.post("/ticket", json=ticket_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        [nameError] = parsed_response.data.get("name")
        [surnameError] = parsed_response.data.get("surname")
        [dateOfBirthError] = parsed_response.data.get("date_of_birth")
        [seatIdError] = parsed_response.data.get("seat_id")
        [flightIdError] = parsed_response.data.get("flight_id")

        self.assertEqual(nameError, "Not a valid string.")
        self.assertEqual(surnameError, "Not a valid string.")
        self.assertEqual(dateOfBirthError, "Not a valid integer.")
        self.assertEqual(seatIdError, "Not a valid UUID.")
        self.assertEqual(flightIdError, "Not a valid UUID.")

        logout(headers)

    def test_passing_empty_params(self):
        headers = get_headers()
        response = app.post("/ticket", json={}, headers=headers)
        parsed_response = ParsedResponse(response)

        missing_data_error = "Missing data for required field."

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        for [value] in parsed_response.data.values():
            self.assertEqual(value, missing_data_error)

        logout(headers)

    def test_passing_empty_headers(self):
        response = app.post("/ticket", json={}, headers={})
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "app-token is not specified in headers")

    def test_passing_empty_auth(self):
        headers = get_initial_headers()

        response = app.post("/ticket", json={}, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "401 UNAUTHORIZED")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Request doesn't contain valid token")

    def test_passing_expired_auth(self):
        JWTConfig.JWT_ACCESS_TOKEN_EXPIRATION = timedelta(seconds=1)
        headers = get_headers()

        time.sleep(1)

        response = app.post("/ticket", json={}, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "401 UNAUTHORIZED")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Token has expired")

        JWTConfig.JWT_ACCESS_TOKEN_EXPIRATION = timedelta(hours=6)
        logout(headers)

    def test_passing_invalid_auth(self):
        headers = get_headers()
        headers["Authorization"] = "Bearer token"

        response = app.post("/ticket", json={}, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "401 UNAUTHORIZED")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Signature verification failed")

        logout(headers)
