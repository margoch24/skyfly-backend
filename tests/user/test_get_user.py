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


class TestGetUser(TestInitializer):
    __title__ = "GET /user"

    def test_get_user_successful(self):
        headers = get_headers()

        response = app.get("/user", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        initial_user = user_config.get_user()
        user = parsed_response.data

        self.assertEqual(user.get("name"), initial_user["name"])
        self.assertEqual(user.get("email"), initial_user["email"])
        self.assertEqual(user.get("photo"), initial_user["photo"])

        self.assertIsNone(user.get("password"))
        self.assertIsNone(user.get("refresh-token"))

        self.assertFalse(user.get("is_deleted"))
        self.assertIsNotNone(user.get("id"))

        self.assertIsInstance(user.get("created_at"), int)
        self.assertIsInstance(user.get("updated_at"), int)

        logout(headers)

    def test_insufficient_permissions(self):
        headers = get_headers()

        User.update_one(headers["user_id"], is_deleted=True)

        response = app.get("/user", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "403 FORBIDDEN")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Insufficient permissions")

        logout(headers)

    def test_passing_empty_headers(self):
        response = app.get("/user", headers={})
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "app-token is not specified in headers")

    def test_passing_empty_auth(self):
        headers = get_initial_headers()
        response = app.get("/user", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "401 UNAUTHORIZED")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Request doesn't contain valid token")

    def test_passing_expired_auth(self):
        JWTConfig.JWT_ACCESS_TOKEN_EXPIRATION = timedelta(seconds=1)
        headers = get_headers()

        time.sleep(1)

        response = app.get("/user", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "401 UNAUTHORIZED")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Token has expired")

        JWTConfig.JWT_ACCESS_TOKEN_EXPIRATION = timedelta(hours=6)

    def test_passing_invalid_auth(self):
        headers = get_headers()
        headers["Authorization"] = "Bearer token"

        response = app.get("/user", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "401 UNAUTHORIZED")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Signature verification failed")
