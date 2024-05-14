from tests.initializer import (
    ParsedResponse,
    Setting,
    TestInitializer,
    app,
    get_initial_headers,
)


class TestGetDiscounts(TestInitializer):
    __title__ = "GET /discounts"

    def test_get_discounts_successful(self):
        headers = get_initial_headers()

        response = app.get("/discounts", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        discounts = parsed_response.data
        self.assertEqual(len(discounts), 1)

        [discountOne] = discounts

        self.assertEqual(discountOne.get("key"), "ticket_child_discount")

    def test_get_only_discounts_successful(self):
        headers = get_initial_headers()
        Setting.create(key="aaa", value="aaa")

        response = app.get("/discounts", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        discounts = parsed_response.data
        self.assertEqual(len(discounts), 1)

        [discountOne] = discounts

        self.assertEqual(discountOne.get("key"), "ticket_child_discount")

    def test_passing_empty_headers(self):
        response = app.get("/discounts", headers={})
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "app-token is not specified in headers")
