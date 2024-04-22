import time

from tests.initializer import (
    JWTConfig,
    ParsedResponse,
    TestInitializer,
    User,
    app,
    get_headers,
    get_initial_headers,
    logout,
    timedelta,
)


class TestPostContactUs(TestInitializer):
    __title__ = "POST /contact_us"

    def test_post_contact_us_successful(self):
        headers = get_initial_headers()

        contact_us_params = {
            "name": "Test User",
            "email": "test@gmail.com",
            "phone_number": "+37044444444",
            "message": "Contact us message",
        }

        response = app.post("/contact_us", json=contact_us_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        contact_us = parsed_response.data

        self.assertEqual(contact_us.get("message"), contact_us_params["message"])
        self.assertEqual(contact_us.get("email"), contact_us_params["email"])
        self.assertEqual(
            contact_us.get("phone_number"), contact_us_params["phone_number"]
        )
        self.assertEqual(contact_us.get("name"), contact_us_params["name"])

        self.assertIsNotNone(contact_us.get("id"))

        self.assertIsInstance(contact_us.get("created_at"), int)
        self.assertIsInstance(contact_us.get("updated_at"), int)

    def test_passing_wrong_params(self):
        headers = get_initial_headers()
        contact_us_params = {
            "name": 45,
            "email": "invalid email",
            "phone_number": [4, 2],
            "message": True,
        }

        response = app.post("/contact_us", json=contact_us_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        [messageError] = parsed_response.data.get("message")
        [nameError] = parsed_response.data.get("name")
        [emailError] = parsed_response.data.get("email")
        [phoneNumberError] = parsed_response.data.get("phone_number")

        self.assertEqual(messageError, "Not a valid string.")
        self.assertEqual(nameError, "Not a valid string.")
        self.assertEqual(emailError, "Not a valid email address.")
        self.assertEqual(phoneNumberError, "Not a valid string.")

    def test_passing_empty_params(self):
        headers = get_initial_headers()
        response = app.post("/contact_us", json={}, headers=headers)
        parsed_response = ParsedResponse(response)

        missing_data_error = "Missing data for required field."

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        [messageError] = parsed_response.data.get("message")
        [nameError] = parsed_response.data.get("name")
        [emailError] = parsed_response.data.get("email")
        [phoneNumberError] = parsed_response.data.get("phone_number")

        self.assertEqual(messageError, missing_data_error)
        self.assertEqual(nameError, missing_data_error)
        self.assertEqual(emailError, missing_data_error)
        self.assertEqual(phoneNumberError, missing_data_error)

    def test_passing_empty_headers(self):
        contact_us_params = {
            "name": "Test User",
            "email": "test@gmail.com",
            "phone_number": "+37044444444",
            "message": "Contact us message",
        }

        response = app.post("/contact_us", json=contact_us_params, headers={})
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "app-token is not specified in headers")
