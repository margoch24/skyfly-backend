import time

from tests.initializer import (
    CabinClass,
    JWTConfig,
    ParsedResponse,
    Scheduled,
    TestInitializer,
    User,
    app,
    get_headers,
    get_initial_headers,
    logout,
    timedelta,
)


class TestPostFlight(TestInitializer):
    __title__ = "POST /flight"

    def test_post_flight_successful(self):
        headers = get_headers(isAdmin=True)

        flight_params = {
            "airline": "United",
            "cabin_class": CabinClass.FIRST,
            "departure": 1713988800000,
            "arrival": 1713996000000,
            "latitude": 34.0573868,
            "longitude": -118.3535625,
            "score": 8.5,
            "scheduled": Scheduled.DAILY,
            "price": 150,
            "currency": "€",
        }

        response = app.post("/flight", json=flight_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        flight = parsed_response.data

        self.assertEqual(flight.get("airline"), flight_params["airline"])
        self.assertEqual(flight.get("cabin_class"), flight_params["cabin_class"])
        self.assertEqual(flight.get("departure"), flight_params["departure"])
        self.assertEqual(flight.get("arrival"), flight_params["arrival"])
        self.assertEqual(flight.get("latitude"), flight_params["latitude"])
        self.assertEqual(flight.get("longitude"), flight_params["longitude"])
        self.assertEqual(flight.get("score"), flight_params["score"])
        self.assertEqual(flight.get("scheduled"), flight_params["scheduled"])
        self.assertEqual(flight.get("price"), flight_params["price"])
        self.assertEqual(flight.get("currency"), flight_params["currency"])

        self.assertIsNotNone(flight.get("id"))

        self.assertIsInstance(flight.get("created_at"), int)
        self.assertIsInstance(flight.get("updated_at"), int)

        logout(headers)

    def test_insufficient_permissions(self):
        headers = get_headers()

        flight_params = {
            "airline": "United",
            "cabin_class": CabinClass.FIRST,
            "departure": 1713988800000,
            "arrival": 1713996000000,
            "latitude": 34.0573868,
            "longitude": -118.3535625,
            "score": 8.5,
            "scheduled": Scheduled.DAILY,
            "price": 150,
            "currency": "€",
        }

        response = app.post("/flight", json=flight_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "403 FORBIDDEN")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Insufficient permissions")

        logout(headers)

    def test_passing_wrong_params(self):
        headers = get_headers()
        flight_params = {
            "airline": 45,
            "cabin_class": "jjjj",
            "departure": "date",
            "arrival": "date",
            "latitude": True,
            "longitude": [],
            "score": 35,
            "scheduled": "hhh",
            "price": "ppp",
            "currency": 58,
        }

        response = app.post("/flight", json=flight_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        [airlineError] = parsed_response.data.get("airline")
        [cabinClassError] = parsed_response.data.get("cabin_class")
        [departureError] = parsed_response.data.get("departure")
        [arrivalError] = parsed_response.data.get("arrival")
        [latitudeError] = parsed_response.data.get("latitude")
        [longitudeError] = parsed_response.data.get("longitude")
        [scoreError] = parsed_response.data.get("score")
        [scheduledError] = parsed_response.data.get("scheduled")
        [priceError] = parsed_response.data.get("price")
        [currencyError] = parsed_response.data.get("currency")

        self.assertEqual(airlineError, "Not a valid string.")
        self.assertEqual(cabinClassError, "Must be one of: business, economy, first.")
        self.assertEqual(departureError, "Not a valid integer.")
        self.assertEqual(arrivalError, "Not a valid integer.")
        self.assertEqual(latitudeError, "Not a valid number.")
        self.assertEqual(longitudeError, "Not a valid number.")
        self.assertEqual(
            scoreError,
            "Must be greater than or equal to 0 and less than or equal to 10.",
        )
        self.assertEqual(
            scheduledError, "Must be one of: daily, monthly, once, weekly."
        )
        self.assertEqual(priceError, "Not a valid number.")
        self.assertEqual(currencyError, "Not a valid string.")

        logout(headers)

    def test_passing_empty_params(self):
        headers = get_headers()
        response = app.post("/flight", json={}, headers=headers)
        parsed_response = ParsedResponse(response)

        missing_data_error = "Missing data for required field."

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        for [value] in parsed_response.data.values():
            self.assertEqual(value, missing_data_error)

        logout(headers)

    def test_passing_empty_headers(self):
        response = app.post("/flight", json={}, headers={})
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "app-token is not specified in headers")

    def test_passing_empty_auth(self):
        headers = get_initial_headers()
        flight_params = {
            "airline": "United",
            "cabin_class": CabinClass.FIRST,
            "departure": 1713988800000,
            "arrival": 1713996000000,
            "latitude": 34.0573868,
            "longitude": -118.3535625,
            "score": 8.5,
            "scheduled": Scheduled.DAILY,
            "price": 150,
            "currency": "€",
        }

        response = app.post("/flight", json=flight_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "401 UNAUTHORIZED")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Request doesn't contain valid token")

    def test_passing_expired_auth(self):
        JWTConfig.JWT_ACCESS_TOKEN_EXPIRATION = timedelta(seconds=1)
        headers = get_headers()

        time.sleep(1)

        flight_params = {
            "airline": "United",
            "cabin_class": CabinClass.FIRST,
            "departure": 1713988800000,
            "arrival": 1713996000000,
            "latitude": 34.0573868,
            "longitude": -118.3535625,
            "score": 8.5,
            "scheduled": Scheduled.DAILY,
            "price": 150,
            "currency": "€",
        }

        response = app.post("/flight", json=flight_params, headers=headers)
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

        flight_params = {
            "airline": "United",
            "cabin_class": CabinClass.FIRST,
            "departure": 1713988800000,
            "arrival": 1713996000000,
            "latitude": 34.0573868,
            "longitude": -118.3535625,
            "score": 8.5,
            "scheduled": Scheduled.DAILY,
            "price": 150,
            "currency": "€",
        }

        response = app.post("/flight", json=flight_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "401 UNAUTHORIZED")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Signature verification failed")

        logout(headers)
