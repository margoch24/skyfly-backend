from flask import request


class PostTicketBody:

    @property
    def name(self):
        return self.__name

    @property
    def surname(self):
        return self.__surname

    @property
    def date_of_birth(self):
        return self.__date_of_birth

    @property
    def seat_id(self):
        return self.__seat_id

    @property
    def flight_id(self):
        return self.__flight_id

    def __init__(self):
        data = request.get_json()
        self.__name = data.get("name")
        self.__surname = data.get("surname")
        self.__date_of_birth = data.get("date_of_birth")
        self.__seat_id = data.get("seat_id")
        self.__flight_id = data.get("flight_id")
