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


class TestPostReview(TestInitializer):
    __title__ = "POST /review"

    def test_post_review_successful(self):
        headers = get_headers()

        review_params = {
            "message": "The flight was convenient. I liked it",
            "rating": 4,
        }

        response = app.post("/review", json=review_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        review = parsed_response.data

        self.assertEqual(review.get("message"), review_params["message"])
        self.assertEqual(review.get("rating"), review_params["rating"])
        self.assertEqual(review.get("user_id"), headers["user_id"])

        self.assertIsNotNone(review.get("id"))

        self.assertIsInstance(review.get("created_at"), int)
        self.assertIsInstance(review.get("updated_at"), int)

        logout(headers)

    def test_insufficient_permissions(self):
        headers = get_headers()

        User.update_one(headers["user_id"], is_deleted=True)

        review_params = {
            "message": "The flight was convenient. I liked it",
            "rating": 4,
        }

        response = app.post("/review", json=review_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "403 FORBIDDEN")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Insufficient permissions")

        logout(headers)

    def test_passing_wrong_params(self):
        headers = get_headers()
        review_params = {
            "message": 445,
            "rating": "string",
        }

        response = app.post("/review", json=review_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        [messageError] = parsed_response.data.get("message")
        [ratingError] = parsed_response.data.get("rating")

        self.assertEqual(messageError, "Not a valid string.")
        self.assertEqual(ratingError, "Not a valid integer.")

        logout(headers)

    def test_passing_empty_params(self):
        headers = get_headers()
        response = app.post("/review", json={}, headers=headers)
        parsed_response = ParsedResponse(response)

        missing_data_error = "Missing data for required field."

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        [messageError] = parsed_response.data.get("message")
        [ratingError] = parsed_response.data.get("rating")

        self.assertEqual(messageError, missing_data_error)
        self.assertEqual(ratingError, missing_data_error)

        logout(headers)

    def test_passing_empty_headers(self):
        response = app.post("/review", json={}, headers={})
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "app-token is not specified in headers")

    def test_passing_empty_auth(self):
        headers = get_initial_headers()
        review_params = {
            "message": "The flight was convenient. I liked it",
            "rating": 4,
        }

        response = app.post("/review", json=review_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "401 UNAUTHORIZED")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Request doesn't contain valid token")

    def test_passing_expired_auth(self):
        JWTConfig.JWT_ACCESS_TOKEN_EXPIRATION = timedelta(seconds=1)
        headers = get_headers()

        time.sleep(1)

        review_params = {
            "message": "The flight was convenient. I liked it",
            "rating": 4,
        }

        response = app.post("/review", json=review_params, headers=headers)
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

        review_params = {
            "message": "The flight was convenient. I liked it",
            "rating": 4,
        }

        response = app.post("/review", json=review_params, headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "401 UNAUTHORIZED")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "Signature verification failed")

        logout(headers)
