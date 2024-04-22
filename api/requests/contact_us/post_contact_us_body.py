from flask import request


class PostContactUsBody:

    @property
    def message(self):
        return self.__message

    @property
    def email(self):
        return self.__email

    @property
    def name(self):
        return self.__name

    @property
    def phone_number(self):
        return self.__phone_number

    def __init__(self):
        data = request.get_json()
        self.__message = data.get("message")
        self.__email = data.get("email")
        self.__phone_number = data.get("phone_number")
        self.__name = data.get("name")
