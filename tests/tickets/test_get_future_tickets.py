import time

from tests.initializer import (
    TEST_QRCODE,
    CabinClass,
    JWTConfig,
    ParsedResponse,
    TestInitializer,
    User,
    app,
    create_flights_with_tickets,
    current_milli_time,
    get_headers,
    get_initial_headers,
    logout,
    timedelta,
)


class TestGetFutureTickets(TestInitializer):
    __title__ = "GET /future-tickets"

    def test_get_future_tickets_successful(self):
        headers = get_headers()
        user_id = headers.get("user_id")

        create_flights_with_tickets(
            user_id=user_id,
            tickets=3,
            additional_flight_data={
                "arrival": current_milli_time() + 2000,
            },
        )
        create_flights_with_tickets(
            user_id=user_id,
            tickets=3,
            additional_flight_data={
                "cabin_class": CabinClass.ECONOMY,
                "arrival": current_milli_time() + 2000,
            },
        )

        response = app.get("/future-tickets", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        tickets = parsed_response.data
        self.assertEqual(len(tickets), 6)

        for index, ticket in enumerate(tickets):
            self.assertEqual(ticket.get("user_id"), headers["user_id"])
            self.assertIsNotNone(ticket.get("name"))
            self.assertIsNotNone(ticket.get("date_of_birth"))
            self.assertIsNotNone(ticket.get("date_of_birth"))
            self.assertIsNotNone(ticket.get("seat_id"))
            self.assertIsNotNone(ticket.get("flight_id"))
            self.assertIsNotNone(ticket.get("currency"))
            self.assertIsNotNone(ticket.get("price"))
            self.assertIsNotNone(ticket.get("type"))
            self.assertIsNotNone(ticket.get("seat").get("row"))

            self.assertGreaterEqual(
                ticket.get("flight").get("arrival"), current_milli_time()
            )

            self.assertEqual(ticket.get("qrcode"), TEST_QRCODE)

            self.assertIsNotNone(ticket.get("id"))

            self.assertIsInstance(ticket.get("created_at"), int)
            self.assertIsInstance(ticket.get("updated_at"), int)

            if index == 0:
                self.assertEqual(
                    ticket.get("flight").get("cabin_class"), CabinClass.ECONOMY
                )

            if index == len(tickets) - 1:
                self.assertEqual(
                    ticket.get("flight").get("cabin_class"), CabinClass.FIRST
                )

        logout(headers)

    def test_get_future_tickets_pagination(self):
        headers = get_headers()
        user_id = headers.get("user_id")

        create_flights_with_tickets(
            user_id=user_id,
            tickets=3,
            additional_flight_data={
                "arrival": current_milli_time() + 2000,
            },
        )
        create_flights_with_tickets(
            user_id=user_id,
            tickets=3,
            additional_flight_data={
                "cabin_class": CabinClass.ECONOMY,
                "arrival": current_milli_time() + 2000,
            },
        )

        limit = 3

        # Page 0
        response = app.get(f"/future-tickets?limit={limit}&page=0", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        tickets_page_0 = parsed_response.data

        self.assertEqual(len(tickets_page_0), 3)

        # Page 1
        response1 = app.get(f"/future-tickets?limit={limit}&page=1", headers=headers)
        parsed_response1 = ParsedResponse(response1)

        self.assertEqual(parsed_response1.error, 0)
        self.assertEqual(response1.status, "200 OK")

        tickets_page_1 = parsed_response1.data

        self.assertEqual(len(tickets_page_1), 3)

        # Page 2
        response2 = app.get(f"/future-tickets?limit={limit}&page=2", headers=headers)
        parsed_response2 = ParsedResponse(response2)

        self.assertEqual(parsed_response2.error, 0)
        self.assertEqual(response2.status, "200 OK")

        tickets_page_2 = parsed_response2.data

        self.assertEqual(len(tickets_page_2), 0)

        logout(headers)

    def test_get_no_tickets_successful(self):
        headers = get_headers()

        response = app.get("/future-tickets", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        tickets = parsed_response.data
        self.assertEqual(len(tickets), 0)

        logout(headers)

    def test_insufficient_permissions(self):
        headers = get_headers()
        user_id = headers.get("user_id")

        User.update_one(user_id, is_deleted=True)

        response = app.get("/future-tickets", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "403 FORBIDDEN")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Insufficient permissions")

        logout(headers)

    def test_passing_wrong_params(self):
        headers = get_headers()
        query = "?page=kkk&limit=k"

        response = app.get(f"/future-tickets{query}", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        [pageError] = parsed_response.data.get("page")
        [limitError] = parsed_response.data.get("limit")

        self.assertEqual(limitError, "Not a valid integer.")
        self.assertEqual(pageError, "Not a valid integer.")

        logout(headers)

    def test_passing_empty_headers(self):
        response = app.get("/future-tickets", headers={})
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "app-token is not specified in headers")

    def test_passing_empty_auth(self):
        headers = get_initial_headers()

        response = app.get("/future-tickets", json={}, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "401 UNAUTHORIZED")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Request doesn't contain valid token")

    def test_passing_expired_auth(self):
        JWTConfig.JWT_ACCESS_TOKEN_EXPIRATION = timedelta(seconds=1)
        headers = get_headers()

        time.sleep(1)

        response = app.get("/future-tickets", json={}, headers=headers)
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

        response = app.get("/future-tickets", json={}, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "401 UNAUTHORIZED")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Signature verification failed")

        logout(headers)
