from flask import request


class GetFlightsQuery:
    @property
    def longitude(self):
        value = self.__longitude
        return value if not value else float(value)

    @property
    def latitude(self):
        value = self.__latitude
        return value if not value else float(value)

    @property
    def departure(self):
        value = self.__departure
        return value if not value else int(value)

    @property
    def arrival(self):
        value = self.__arrival
        return value if not value else int(value)

    @property
    def cabin_class(self):
        if not self.__cabin_class:
            return self.__cabin_class

        values = self.__cabin_class.split(",")
        return values

    @property
    def price(self):
        if not self.__price:
            return self.__price

        [min, max] = self.__price.split(",")

        min_to_num = float(min)
        max_to_num = float(max)
        return [min_to_num, max_to_num]

    @property
    def page(self):
        value = self.__page
        return value if not value else int(value)

    @property
    def limit(self):
        value = self.__limit
        return value if not value else int(value)

    def __init__(self):
        data = request.args
        self.__longitude = data.get("longitude")
        self.__latitude = data.get("latitude")
        self.__departure = data.get("departure")
        self.__arrival = data.get("arrival")
        self.__cabin_class = data.get("cabin_class")
        self.__price = data.get("price")
        self.__page = data.get("page")
        self.__limit = data.get("limit")
