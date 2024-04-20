from tests.initializer import (
    ParsedResponse,
    TestInitializer,
    app,
    get_headers,
    get_initial_headers,
    logout,
)


class TestRefreshAccess(TestInitializer):
    __title__ = "POST /refresh-access"

    def test_successful_refresh_access(self):
        get_headers()
        headers = get_initial_headers()

        response = app.post("/refresh-access", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        access_token = parsed_response.data.get("access_token")
        self.assertIsInstance(access_token, str)

        logout(headers)

    def test_cannot_refresh_without_login(self):
        headers = get_initial_headers()

        response = app.post("/refresh-access", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "401 UNAUTHORIZED")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Refresh token is missing")

    def test_passing_empty_headers(self):
        response = app.post("/refresh-access", headers={})
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "app_token is not specified in headers")
