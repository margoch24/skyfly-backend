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
    user_config,
)


class TestPutUser(TestInitializer):
    __title__ = "PUT /user"

    def test_put_user_successful(self):
        headers = get_headers()
        user_id = headers.get("user_id")

        update_params = {
            "name": "Updated name",
            "phone_number": "+37088699444",
            "photo": "new_photo.png",
        }

        response = app.put("/user", json=update_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        updated_user = User.find_one({"id": user_id})

        self.assertEqual(updated_user.name, update_params["name"])
        self.assertEqual(updated_user.phone_number, update_params["phone_number"])
        self.assertEqual(updated_user.photo, update_params["photo"])

        logout(headers)

    def test_insufficient_permissions(self):
        headers = get_headers()

        User.update_one(headers["user_id"], is_deleted=True)

        update_params = {
            "name": "Updated name",
            "phone_number": "+37088699444",
            "photo": "new_photo.png",
        }

        response = app.put("/user", json=update_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "403 FORBIDDEN")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Insufficient permissions")

        logout(headers)

    def test_passing_wrong_params(self):
        headers = get_headers()
        update_params = {
            "name": [],
            "phone_number": 458,
            "photo": True,
        }

        response = app.put("/user", json=update_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        [nameError] = parsed_response.data.get("name")
        [phoneNumberError] = parsed_response.data.get("phone_number")
        [photoError] = parsed_response.data.get("photo")

        self.assertEqual(nameError, "Not a valid string.")
        self.assertEqual(phoneNumberError, "Not a valid string.")
        self.assertEqual(photoError, "Not a valid string.")

        logout(headers)

    def test_passing_empty_params(self):
        headers = get_headers()
        user_id = headers.get("user_id")

        response = app.put("/user", json={}, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        initial_user = user_config.get_user()
        updated_user = User.find_one({"id": user_id})

        self.assertEqual(updated_user.name, initial_user["name"])
        self.assertEqual(updated_user.phone_number, initial_user["phone_number"])
        self.assertEqual(updated_user.photo, initial_user["photo"])

        logout(headers)

    def test_passing_empty_headers(self):
        response = app.put("/user", headers={})
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "app-token is not specified in headers")

    def test_passing_empty_auth(self):
        headers = get_initial_headers()
        response = app.put("/user", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "401 UNAUTHORIZED")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Request doesn't contain valid token")

    def test_passing_expired_auth(self):
        JWTConfig.JWT_ACCESS_TOKEN_EXPIRATION = timedelta(seconds=1)
        headers = get_headers()

        time.sleep(1)

        response = app.put("/user", headers=headers)
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

        response = app.put("/user", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "401 UNAUTHORIZED")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Signature verification failed")
        logout(headers)
