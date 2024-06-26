from flask import request


class PostRegisterBody:

    @property
    def email(self):
        return self.__email

    @property
    def password(self):
        return self.__password

    @property
    def name(self):
        return self.__name

    @property
    def phone_number(self):
        return self.__phone_number

    def __init__(self):
        data = request.get_json()
        self.__password = data.get("password")
        self.__email = data.get("email")
        self.__name = data.get("name")
        self.__phone_number = data.get("phone_number")
