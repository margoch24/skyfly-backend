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
    def from_longitude(self):
        return self.__from_longitude

    @property
    def from_latitude(self):
        return self.__from_latitude

    @property
    def to_longitude(self):
        return self.__to_longitude

    @property
    def to_latitude(self):
        return self.__to_latitude

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
        self.__from_longitude = data.get("from_longitude")
        self.__from_latitude = data.get("from_latitude")
        self.__to_longitude = data.get("to_longitude")
        self.__to_latitude = data.get("to_latitude")
        self.__score = data.get("score")
