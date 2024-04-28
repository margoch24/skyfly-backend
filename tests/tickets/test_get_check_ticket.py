import time

from tests.initializer import (
    JWTConfig,
    ParsedResponse,
    TestInitializer,
    Ticket,
    app,
    create_flights_with_tickets,
    current_milli_time,
    get_headers,
    get_initial_headers,
    logout,
    timedelta,
)


class TestCheckTicket(TestInitializer):
    __title__ = "GET /check-ticket"

    def test_check_ticket_successful(self):
        headers = get_headers(isAdmin=True)

        user_headers = get_headers()
        user_id = user_headers.get("user_id")
        create_flights_with_tickets(user_id, tickets=1)

        ticket = Ticket.find_one()

        response = app.get(f"/check-ticket?ticket_id={ticket.id}", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        ticket = parsed_response.data

        self.assertEqual(ticket.get("message"), "Ticket is valid")
        self.assertTrue(ticket.get("valid"))

        self.assertIsNotNone(ticket.get("owner_name"))
        self.assertIsNotNone(ticket.get("owner_email"))
        self.assertIsNotNone(ticket.get("initial_price"))
        self.assertIsNotNone(ticket.get("seat"))
        self.assertIsNotNone(ticket.get("flight"))

        logout(headers)
        logout(user_headers)

    def test_check_deleted_ticket_successful(self):
        headers = get_headers(isAdmin=True)

        user_headers = get_headers()
        user_id = user_headers.get("user_id")
        create_flights_with_tickets(user_id, tickets=1)

        ticket = Ticket.find_one()
        Ticket.update_one(ticket.id, is_deleted=True)

        response = app.get(f"/check-ticket?ticket_id={ticket.id}", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        ticket = parsed_response.data

        self.assertEqual(ticket.get("message"), "Ticket is deleted")
        self.assertFalse(ticket.get("valid"))

        self.assertIsNotNone(ticket.get("owner_name"))
        self.assertIsNotNone(ticket.get("owner_email"))
        self.assertIsNotNone(ticket.get("initial_price"))
        self.assertIsNotNone(ticket.get("seat"))
        self.assertIsNotNone(ticket.get("flight"))

        logout(headers)
        logout(user_headers)

    def test_check_expired_ticket_successful(self):
        headers = get_headers(isAdmin=True)

        user_headers = get_headers()
        user_id = user_headers.get("user_id")
        create_flights_with_tickets(
            user_id,
            tickets=1,
            additional_flight_data={"arrival": current_milli_time() - 1000},
        )

        ticket = Ticket.find_one()
        Ticket.update_one(ticket.id, is_deleted=True)

        response = app.get(f"/check-ticket?ticket_id={ticket.id}", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        ticket = parsed_response.data

        self.assertEqual(ticket.get("message"), "Ticket is expired")
        self.assertFalse(ticket.get("valid"))

        self.assertIsNotNone(ticket.get("owner_name"))
        self.assertIsNotNone(ticket.get("owner_email"))
        self.assertIsNotNone(ticket.get("initial_price"))
        self.assertIsNotNone(ticket.get("seat"))
        self.assertIsNotNone(ticket.get("flight"))

        logout(headers)
        logout(user_headers)

    def test_insufficient_permissions(self):
        headers = get_headers()

        response = app.get(
            f"/check-ticket?ticket_id=78dbf89d4aec4c4f9e3b1c370ccf3c36", headers=headers
        )
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "403 FORBIDDEN")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Insufficient permissions")

        logout(headers)

    def test_passing_wrong_params(self):
        headers = get_headers(isAdmin=True)

        response = app.get(f"/check-ticket?ticket_id=llll", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        [ticketIdError] = parsed_response.data.get("ticket_id")

        self.assertEqual(ticketIdError, "Not a valid UUID.")

        logout(headers)

    def test_passing_empty_params(self):
        headers = get_headers(isAdmin=True)

        response = app.get("/check-ticket", headers=headers)
        parsed_response = ParsedResponse(response)

        missing_data_error = "Missing data for required field."

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        for [value] in parsed_response.data.values():
            self.assertEqual(value, missing_data_error)

        logout(headers)

    def test_passing_empty_headers(self):
        response = app.get("/check-ticket", headers={})
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "app-token is not specified in headers")

    def test_passing_empty_auth(self):
        headers = get_initial_headers()

        response = app.get("/check-ticket", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "401 UNAUTHORIZED")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Request doesn't contain valid token")

    def test_passing_expired_auth(self):
        JWTConfig.JWT_ACCESS_TOKEN_EXPIRATION = timedelta(seconds=1)
        headers = get_headers()

        time.sleep(1)

        response = app.get("/check-ticket", headers=headers)
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

        response = app.get("/check-ticket", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "401 UNAUTHORIZED")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Signature verification failed")

        logout(headers)
