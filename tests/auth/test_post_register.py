from tests.initializer import ParsedResponse, TestInitializer, app, get_initial_headers


class TestRegister(TestInitializer):
    __title__ = "POST /register"

    def test_successful_register(self):
        register_params = {
            "email": "test@gmail.com",
            "password": "test1234",
            "name": "Test User",
            "phone_number": "+3706458790",
        }

        headers = get_initial_headers()
        response = app.post("/register", json=register_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        user = parsed_response.data

        self.assertEqual(user.get("name"), register_params["name"])
        self.assertEqual(user.get("email"), register_params["email"])
        self.assertEqual(user.get("phone_number"), register_params["phone_number"])

        self.assertTrue("photo" in user)

        self.assertIsNone(user.get("password"))
        self.assertIsNone(user.get("refresh-token"))

        self.assertFalse(user.get("is_deleted"))
        self.assertIsNotNone(user.get("id"))

        self.assertIsInstance(user.get("created_at"), int)
        self.assertIsInstance(user.get("updated_at"), int)

    def test_account_exists(self):
        register_params = {
            "email": "test@gmail.com",
            "password": "test1234",
            "name": "Test User",
            "phone_number": "+3706458790",
        }

        headers = get_initial_headers()
        app.post("/register", json=register_params, headers=headers)

        response = app.post("/register", json=register_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "409 CONFLICT")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Account already exists")

    def test_passing_wrong_params(self):
        register_params = {
            "email": "empty string",
            "password": True,
            "name": 45,
            "phone_number": ["array"],
        }

        headers = get_initial_headers()
        response = app.post("/register", json=register_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        [emailError] = parsed_response.data.get("email")
        [passwordError] = parsed_response.data.get("password")
        [nameError] = parsed_response.data.get("name")

        self.assertEqual(emailError, "Not a valid email address.")
        self.assertEqual(passwordError, "Not a valid string.")
        self.assertEqual(nameError, "Not a valid string.")

    def test_passing_empty_params(self):
        headers = get_initial_headers()
        response = app.post("/register", json={}, headers=headers)
        parsed_response = ParsedResponse(response)

        missing_data_error = "Missing data for required field."

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        [emailError] = parsed_response.data.get("email")
        [passwordError] = parsed_response.data.get("password")
        [nameError] = parsed_response.data.get("name")

        self.assertEqual(emailError, missing_data_error)
        self.assertEqual(passwordError, missing_data_error)
        self.assertEqual(nameError, missing_data_error)

    def test_passing_no_params(self):
        headers = get_initial_headers()
        response = app.post("/register", headers=headers)

        self.assertEqual(response.status, "415 UNSUPPORTED MEDIA TYPE")

    def test_passing_empty_headers(self):
        register_params = {
            "email": "test@gmail.com",
            "password": "test1234",
            "name": "Test User",
            "phone_number": "+3706458790",
        }

        response = app.post("/register", json=register_params, headers={})
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "app-token is not specified in headers")
