import time

from tests.initializer import (
    JWTConfig,
    ParsedResponse,
    TestInitializer,
    TokenBlocklist,
    app,
    get_headers,
    get_initial_headers,
    timedelta,
)


class TestLogout(TestInitializer):
    __title__ = "POST /logout"

    def test_successful_logout(self):
        headers = get_headers()

        response = app.post("/logout", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        revoked_tokens = TokenBlocklist.find()
        self.assertEqual(len(revoked_tokens), 2)

        user_response = app.get("/user", headers=headers)
        parsed_user_response = ParsedResponse(user_response)

        self.assertEqual(parsed_user_response.error, 1)
        self.assertEqual(user_response.status, "401 UNAUTHORIZED")

        message = parsed_user_response.data.get("message")
        self.assertEqual(message, "Token has been revoked")

    def test_passing_empty_auth(self):
        headers = get_initial_headers()
        response = app.post("/logout", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "401 UNAUTHORIZED")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Request doesn't contain valid token")

    def test_passing_expired_auth(self):
        JWTConfig.JWT_ACCESS_TOKEN_EXPIRATION = timedelta(seconds=1)
        headers = get_headers()

        time.sleep(1)

        response = app.post("/logout", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "401 UNAUTHORIZED")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Token has expired")

    def test_passing_invalid_auth(self):
        headers = get_headers()
        headers["Authorization"] = "Bearer token"

        response = app.post("/logout", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "401 UNAUTHORIZED")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Signature verification failed")
