from flask import request


class PostFlightBody:

    @property
    def departure(self):
        return self.__departure

    @property
    def arrival(self):
        return self.__arrival

    @property
    def photo(self):
        return self.__photo

    @property
    def airline(self):
        return self.__airline

    @property
    def cabin_class(self):
        return self.__cabin_class

    @property
    def scheduled(self):
        return self.__scheduled

    @property
    def price(self):
        return self.__price

    @property
    def currency(self):
        return self.__currency

    @property
    def longitude(self):
        return self.__longitude

    @property
    def latitude(self):
        return self.__latitude

    @property
    def score(self):
        return self.__score

    def __init__(self):
        data = request.get_json()
        self.__arrival = data.get("arrival")
        self.__photo = data.get("photo")
        self.__departure = data.get("departure")
        self.__airline = data.get("airline")
        self.__cabin_class = data.get("cabin_class")
        self.__scheduled = data.get("scheduled")
        self.__price = data.get("price")
        self.__currency = data.get("currency")
        self.__longitude = data.get("longitude")
        self.__latitude = data.get("latitude")
        self.__score = data.get("score")
