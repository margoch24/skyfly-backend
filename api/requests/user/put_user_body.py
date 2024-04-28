from flask import request


class PutUserBody:

    @property
    def name(self):
        return self.__name

    @property
    def phone_number(self):
        return self.__phone_number

    @property
    def photo(self):
        return self.__photo

    def __init__(self):
        data = request.get_json()
        self.__name = data.get("name")
        self.__phone_number = data.get("phone_number")
        self.__photo = data.get("photo")
