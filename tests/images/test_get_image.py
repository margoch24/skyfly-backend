from tests.initializer import ParsedResponse, TestInitializer, app, get_initial_headers


class TestGetImage(TestInitializer):
    __title__ = "GET /image"

    def test_passing_wrong_params(self):
        headers = get_initial_headers()

        response = app.get("/image?filename=non_existing_file", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(response.status, "404 NOT FOUND")

        self.assertEqual(
            parsed_response.message,
            "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
        )

    def test_passing_empty_params(self):
        headers = get_initial_headers()

        response = app.get("/image", headers=headers)
        parsed_response = ParsedResponse(response)

        missing_data_error = "Missing data for required field."

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        [filenameError] = parsed_response.data.get("filename")

        self.assertEqual(filenameError, missing_data_error)

    def test_passing_empty_headers(self):
        response = app.get("/image", headers={})
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "app-token is not specified in headers")
