from tests.initializer import (
    Admin,
    ParsedResponse,
    TestInitializer,
    User,
    app,
    bcrypt,
    get_initial_headers,
    logout,
)


class TestLogin(TestInitializer):
    __title__ = "POST /login"

    def test_successful_login_user(self):
        login_params = {
            "email": "test@gmail.com",
            "password": "test1234",
        }

        User.create(
            email=login_params["email"],
            password=bcrypt.hash_password(login_params["password"]),
            name="Test User",
        )

        headers = get_initial_headers()
        response = app.post("/login", json=login_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        access_token = parsed_response.data.get("access_token")
        self.assertIsInstance(access_token, str)

        logout(headers, access_token)

    def test_successful_login_admin(self):
        login_params = {
            "email": "test@gmail.com",
            "password": "test1234",
        }

        Admin.create(
            email=login_params["email"],
            password=bcrypt.hash_password(login_params["password"]),
        )

        headers = get_initial_headers()
        headers["referrer-type"] = "admin"

        response = app.post("/login", json=login_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        access_token = parsed_response.data.get("access_token")
        self.assertIsInstance(access_token, str)

        logout(headers, access_token)

    def test_no_account_exists(self):
        login_params = {
            "email": "test@gmail.com",
            "password": "test1234",
        }

        headers = get_initial_headers()
        response = app.post("/login", json=login_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "403 FORBIDDEN")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Account does not exist")

    def test_invalid_password(self):
        login_params = {
            "email": "test@gmail.com",
            "password": "test1234",
        }

        User.create(
            email=login_params["email"],
            password=bcrypt.hash_password("another_password"),
            name="Test User",
        )

        headers = get_initial_headers()
        response = app.post("/login", json=login_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "403 FORBIDDEN")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Invalid password information entered")

    def test_passing_wrong_params(self):
        login_params = {
            "email": 45,
            "password": True,
        }

        headers = get_initial_headers()
        response = app.post("/login", json=login_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        [emailError] = parsed_response.data.get("email")
        [passwordError] = parsed_response.data.get("password")

        self.assertEqual(emailError, "Not a valid email address.")
        self.assertEqual(passwordError, "Not a valid string.")

    def test_passing_empty_params(self):
        headers = get_initial_headers()
        response = app.post("/login", json={}, headers=headers)
        parsed_response = ParsedResponse(response)

        missing_data_error = "Missing data for required field."

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        [emailError] = parsed_response.data.get("email")
        [passwordError] = parsed_response.data.get("password")

        self.assertEqual(emailError, missing_data_error)
        self.assertEqual(passwordError, missing_data_error)

    def test_passing_no_params(self):
        headers = get_initial_headers()
        response = app.post("/login", headers=headers)

        self.assertEqual(response.status, "415 UNSUPPORTED MEDIA TYPE")

    def test_passing_empty_headers(self):
        login_params = {
            "email": "test@gmail.com",
            "password": "test1234",
        }

        response = app.post("/login", json=login_params, headers={})
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "app-token is not specified in headers")

    def test_passing_empty_headers(self):
        response = app.post("/logout", headers={})
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "app-token is not specified in headers")
