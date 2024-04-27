from tests.initializer import (
    CabinClass,
    Flight,
    ParsedResponse,
    Seat,
    TestInitializer,
    app,
    create_flights_with_tickets,
    current_milli_time,
    get_headers,
    get_initial_headers,
    logout,
)


class TestGetFlights(TestInitializer):
    __title__ = "GET /flights"

    def test_get_flights_successful(self):
        headers = get_headers()
        user_id = headers.get("user_id")

        flight_one_tickets = 1
        flight_one = create_flights_with_tickets(
            user_id=user_id, tickets=flight_one_tickets
        )

        flight_two_tickets = 1
        flight_two = create_flights_with_tickets(
            user_id=user_id,
            additional_flight_data={"cabin_class": CabinClass.ECONOMY},
            tickets=flight_two_tickets,
        )

        flight_three_tickets = 1
        flight_three = create_flights_with_tickets(
            user_id=user_id,
            additional_flight_data={"cabin_class": CabinClass.BUSINESS},
            tickets=flight_three_tickets,
        )

        flight_four_tickets = 2
        create_flights_with_tickets(
            user_id=user_id,
            additional_flight_data={"cabin_class": CabinClass.BUSINESS},
            tickets=flight_four_tickets,
        )

        response = app.get("/flights", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        flights = parsed_response.data
        self.assertEqual(len(flights), 4)

        [flightFour, flightThree, flightTwo, flightOne] = flights

        self.assertEqual(flightThree.get("cabin_class"), flight_three.cabin_class)
        self.assertEqual(flightThree.get("id"), flight_three.id)

        self.assertEqual(flightTwo.get("cabin_class"), flight_two.cabin_class)
        self.assertEqual(flightTwo.get("id"), flight_two.id)

        self.assertEqual(flightOne.get("cabin_class"), flight_one.cabin_class)
        self.assertEqual(flightOne.get("id"), flight_one.id)

        buisness_seats = len(Seat.find({"cabin_class": CabinClass.BUSINESS}))
        first_seats = len(Seat.find({"cabin_class": CabinClass.FIRST}))
        economy_seats = len(Seat.find({"cabin_class": CabinClass.ECONOMY}))

        self.assertEqual(
            flightFour.get("available_seats"), buisness_seats - flight_four_tickets
        )
        self.assertEqual(
            flightThree.get("available_seats"), buisness_seats - flight_three_tickets
        )
        self.assertEqual(
            flightTwo.get("available_seats"), economy_seats - flight_two_tickets
        )
        self.assertEqual(
            flightOne.get("available_seats"), first_seats - flight_one_tickets
        )

        logout(headers)

    def test_get_flights_pagination(self):
        headers = get_headers()
        user_id = headers.get("user_id")

        flight_one = create_flights_with_tickets(user_id=user_id)
        flight_two = create_flights_with_tickets(
            user_id=user_id,
            additional_flight_data={"cabin_class": CabinClass.ECONOMY},
        )
        flight_three = create_flights_with_tickets(
            user_id=user_id,
            additional_flight_data={"cabin_class": CabinClass.BUSINESS},
        )

        limit = 2

        # Page 0
        response = app.get(f"/flights?limit={limit}&page=0", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        flights_page_0 = parsed_response.data

        self.assertEqual(len(flights_page_0), 2)

        [flightThree, flightTwo] = flights_page_0
        self.assertEqual(flightThree.get("id"), flight_three.id)
        self.assertEqual(flightTwo.get("id"), flight_two.id)

        # Page 1
        response1 = app.get(f"/flights?limit={limit}&page=1", headers=headers)
        parsed_response1 = ParsedResponse(response1)

        self.assertEqual(parsed_response1.error, 0)
        self.assertEqual(response1.status, "200 OK")

        flights_page_1 = parsed_response1.data

        self.assertEqual(len(flights_page_1), 1)

        [flightOne] = flights_page_1
        self.assertEqual(flightOne.get("id"), flight_one.id)

        # Page 2
        response2 = app.get(f"/flights?limit={limit}&page=2", headers=headers)
        parsed_response2 = ParsedResponse(response2)

        self.assertEqual(parsed_response2.error, 0)
        self.assertEqual(response2.status, "200 OK")

        flights_page_2 = parsed_response2.data

        self.assertEqual(len(flights_page_2), 0)

        logout(headers)

    def test_get_flights_by_price(self):
        headers = get_headers()
        user_id = headers.get("user_id")

        flight_one = create_flights_with_tickets(user_id=user_id)
        flight_two = create_flights_with_tickets(
            user_id=user_id,
            additional_flight_data={"price": 245},
        )
        flight_three = create_flights_with_tickets(
            user_id=user_id,
            additional_flight_data={"price": 400},
        )

        limit = 2

        # Price 300-400
        response = app.get(f"/flights?limit={limit}&price=300,400", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        flights = parsed_response.data
        self.assertEqual(len(flights), 1)

        [flightThree] = flights
        self.assertEqual(flightThree.get("price"), flight_three.price)

        # Price 100-300
        response2 = app.get(f"/flights?limit={limit}&price=100,300", headers=headers)
        parsed_response2 = ParsedResponse(response2)

        self.assertEqual(parsed_response2.error, 0)
        self.assertEqual(response2.status, "200 OK")

        flights2 = parsed_response2.data
        self.assertEqual(len(flights2), 2)

        [flightTwo, flightOne] = flights2
        self.assertEqual(flightTwo.get("price"), flight_two.price)
        self.assertEqual(flightOne.get("price"), flight_one.price)

        # Price 50-100
        response3 = app.get(f"/flights?limit={limit}&price=50,100", headers=headers)
        parsed_response3 = ParsedResponse(response3)

        self.assertEqual(parsed_response3.error, 0)
        self.assertEqual(response3.status, "200 OK")

        flights3 = parsed_response3.data
        self.assertEqual(len(flights3), 0)

        logout(headers)

    def test_get_flights_by_cabin_class(self):
        headers = get_headers()
        user_id = headers.get("user_id")

        flight_one = create_flights_with_tickets(user_id=user_id)
        flight_two = create_flights_with_tickets(
            user_id=user_id,
            additional_flight_data={"cabin_class": CabinClass.BUSINESS},
        )
        flight_three = create_flights_with_tickets(
            user_id=user_id,
            additional_flight_data={"cabin_class": CabinClass.ECONOMY},
        )

        limit = 2

        # Cabin class: first
        response = app.get(
            f"/flights?limit={limit}&cabin_class={CabinClass.FIRST}",
            headers=headers,
        )
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        flights = parsed_response.data
        self.assertEqual(len(flights), 1)

        [flightOne] = flights
        self.assertEqual(flightOne.get("cabin_class"), flight_one.cabin_class)

        # Cabin class: economy, business
        response2 = app.get(
            f"/flights?limit={limit}&cabin_class={CabinClass.ECONOMY},{CabinClass.BUSINESS}",
            headers=headers,
        )
        parsed_response2 = ParsedResponse(response2)

        self.assertEqual(parsed_response2.error, 0)
        self.assertEqual(response2.status, "200 OK")

        flights2 = parsed_response2.data
        self.assertEqual(len(flights2), 2)

        [flightThree, flightTwo] = flights2
        self.assertEqual(flightThree.get("cabin_class"), flight_three.cabin_class)
        self.assertEqual(flightTwo.get("cabin_class"), flight_two.cabin_class)

        logout(headers)

    def test_get_flights_by_arrival(self):
        headers = get_headers()
        user_id = headers.get("user_id")
        one_day = 24 * 60 * 60 * 1000

        create_flights_with_tickets(user_id=user_id)

        arrival_flight_two = current_milli_time() + one_day
        create_flights_with_tickets(
            user_id=user_id,
            additional_flight_data={
                "arrival": arrival_flight_two,
                "cabin_class": CabinClass.BUSINESS,
            },
        )

        arrival_flight_three = current_milli_time() + one_day * 2
        flight_three = create_flights_with_tickets(
            user_id=user_id,
            additional_flight_data={
                "arrival": arrival_flight_three,
                "cabin_class": CabinClass.ECONOMY,
            },
        )

        limit = 2

        # Arrival 1
        response = app.get(
            f"/flights?limit={limit}&arrival={arrival_flight_three}",
            headers=headers,
        )
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        flights = parsed_response.data
        self.assertEqual(len(flights), 1)

        [flightThree] = flights
        self.assertEqual(flightThree.get("cabin_class"), flight_three.cabin_class)

        # Arrival 2
        response2 = app.get(
            f"/flights?limit={limit}&arrival={arrival_flight_two}",
            headers=headers,
        )
        parsed_response2 = ParsedResponse(response2)

        self.assertEqual(parsed_response2.error, 0)
        self.assertEqual(response2.status, "200 OK")

        flights2 = parsed_response2.data
        self.assertEqual(len(flights2), 2)

        logout(headers)

    def test_get_flights_by_departure(self):
        headers = get_headers()
        user_id = headers.get("user_id")
        one_day = 24 * 60 * 60 * 1000

        create_flights_with_tickets(user_id=user_id)

        departure_flight_two = current_milli_time() + one_day
        create_flights_with_tickets(
            user_id=user_id,
            additional_flight_data={
                "departure": departure_flight_two,
                "cabin_class": CabinClass.BUSINESS,
            },
        )

        departure_flight_three = current_milli_time() + one_day * 2
        flight_three = create_flights_with_tickets(
            user_id=user_id,
            additional_flight_data={
                "departure": departure_flight_three,
                "cabin_class": CabinClass.ECONOMY,
            },
        )

        limit = 2

        # Departure 1
        response = app.get(
            f"/flights?limit={limit}&departure={departure_flight_three}",
            headers=headers,
        )
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        flights = parsed_response.data
        self.assertEqual(len(flights), 1)

        [flightThree] = flights
        self.assertEqual(flightThree.get("cabin_class"), flight_three.cabin_class)

        # Departure 2
        response2 = app.get(
            f"/flights?limit={limit}&departure={departure_flight_two}",
            headers=headers,
        )
        parsed_response2 = ParsedResponse(response2)

        self.assertEqual(parsed_response2.error, 0)
        self.assertEqual(response2.status, "200 OK")

        flights2 = parsed_response2.data
        self.assertEqual(len(flights2), 1)

        logout(headers)

    def test_get_flights_by_latitude_longitude(self):
        headers = get_headers()
        user_id = headers.get("user_id")

        flight_one = create_flights_with_tickets(user_id=user_id)

        response = app.get(
            f"/flights?latitude={flight_one.latitude}&longitude={flight_one.longitude}",
            headers=headers,
        )
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        flights = parsed_response.data
        self.assertEqual(len(flights), 1)

        [flightOne] = flights
        self.assertEqual(flightOne.get("id"), flight_one.id)

        logout(headers)

    def test_get_no_flights_successful(self):
        headers = get_initial_headers()

        response = app.get("/flights", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        flights = parsed_response.data
        self.assertEqual(len(flights), 0)

    def test_cannot_get_expired_flights(self):
        headers = get_headers()
        user_id = headers.get("user_id")

        create_flights_with_tickets(
            user_id=user_id,
            tickets=0,
            additional_flight_data={"arrival": current_milli_time() - 1000},
        )

        response = app.get("/flights", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        flights = parsed_response.data
        self.assertEqual(len(flights), 0)

        logout(headers)

    def test_cannot_get_deleted_flights(self):
        headers = get_headers()
        user_id = headers.get("user_id")

        created_fligth = create_flights_with_tickets(
            user_id=user_id,
            tickets=0,
        )

        Flight.update_one(created_fligth.id, is_deleted=True)

        response = app.get("/flights", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 0)
        self.assertEqual(response.status, "200 OK")

        flights = parsed_response.data
        self.assertEqual(len(flights), 0)

        logout(headers)

    def test_passing_wrong_params(self):
        headers = get_initial_headers()
        query = """?page=kkk
                    &price=300,25
                    &cabin_class=kkk
                    &arrival=True
                    &departure=[]
                    &latitude=kkk
                    &longitude=kkk
                    &limit=k"""

        response = app.get(f"/flights{query}", headers=headers)
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        [longitudeError] = parsed_response.data.get("longitude")
        [latitudeError] = parsed_response.data.get("latitude")
        [departureError] = parsed_response.data.get("departure")
        [arrivalError] = parsed_response.data.get("arrival")
        [cabinClassError] = parsed_response.data.get("cabin_class")
        [priceError] = parsed_response.data.get("price")
        [pageError] = parsed_response.data.get("page")
        [limitError] = parsed_response.data.get("limit")

        self.assertEqual(longitudeError, "Not a valid number.")
        self.assertEqual(latitudeError, "Not a valid number.")
        self.assertEqual(departureError, "Not a valid integer.")
        self.assertEqual(arrivalError, "Not a valid integer.")
        self.assertEqual(cabinClassError, "Must be one of: business, economy, first.")
        self.assertEqual(
            priceError, "Invalid price range format. Use 'price=min,max' format."
        )
        self.assertEqual(limitError, "Not a valid integer.")
        self.assertEqual(pageError, "Not a valid integer.")

    def test_passing_empty_headers(self):
        response = app.get("/flights", headers={})
        parsed_response = ParsedResponse(response)

        self.assertEqual(parsed_response.error, 1)
        self.assertEqual(response.status, "400 BAD REQUEST")

        message = parsed_response.data.get("message")
        self.assertEqual(message, "app-token is not specified in headers")
