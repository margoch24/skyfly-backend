from io import BytesIO

from tests.initializer import ParsedResponse, TestInitializer, app, get_initial_headers


class TestUploadImage(TestInitializer):
    __title__ = "POST /upload-image"

    def test_no_selected_file(self):
        headers = get_initial_headers()

        response = app.post(
            "/upload-image",
            headers=headers,
            data={"file": (BytesIO("".encode()), "")},
            content_type="multipart/form-data",
        )
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        message = parsed_response.data.get("message")

        self.assertEqual(message, "No selected file")

    def test_invalid_file_type(self):
        headers = get_initial_headers()

        response = app.post(
            "/upload-image",
            headers=headers,
            data={"file": (BytesIO("".encode()), "img.pdf")},
            content_type="multipart/form-data",
        )
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        message = parsed_response.data.get("message")

        self.assertEqual(message, "Invalid file type")

    def test_passing_empty_params(self):
        headers = get_initial_headers()

        response = app.post("/upload-image", headers=headers)
        parsed_response = ParsedResponse(response)

        missing_data_error = "Missing data for required field."

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        [fileError] = parsed_response.data.get("file")

        self.assertEqual(fileError, missing_data_error)

    def test_passing_empty_headers(self):
        response = app.post("/upload-image", headers={})
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "app-token is not specified in headers")
