from flask import request


class GetFlightQuery:
    @property
    def flight_id(self):
        return self.__flight_id

    def __init__(self):
        data = request.args
        self.__flight_id = data.get("flight_id")
