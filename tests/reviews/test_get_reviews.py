from tests.initializer import ParsedResponse, TestInitializer, app, get_headers, logout


class TestGetReviews(TestInitializer):
    __title__ = "GET /reviews"

    def test_get_reviews_successful(self):
        headers = get_headers()
        user_id = headers["user_id"]

        review_one_params = {
            "message": "The flight was convenient. I liked it",
            "rating": 4,
        }

        review_two_params = {
            "message": "The flight was perfect",
            "rating": 3,
        }

        app.post("/review", json=review_one_params, headers=headers)
        app.post("/review", json=review_two_params, headers=headers)

        response = app.get("/reviews", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        reviews = parsed_response.data
        self.assertEqual(len(reviews), 2)

        [reviewTwo, reviewOne] = reviews

        self.assertEqual(reviewTwo.get("message"), review_two_params["message"])
        self.assertEqual(reviewTwo.get("rating"), review_two_params["rating"])
        self.assertEqual(reviewTwo.get("user_id"), user_id)

        self.assertEqual(reviewOne.get("message"), review_one_params["message"])
        self.assertEqual(reviewOne.get("rating"), review_one_params["rating"])
        self.assertEqual(reviewOne.get("user_id"), user_id)

        logout(headers)

    def test_get_no_reviews_successful(self):
        headers = get_headers()

        response = app.get("/reviews", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        reviews = parsed_response.data
        self.assertEqual(len(reviews), 0)

        logout(headers)

    def test_passing_empty_headers(self):
        response = app.get("/reviews", headers={})
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "app-token is not specified in headers")
