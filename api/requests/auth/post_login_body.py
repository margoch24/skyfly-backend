from flask import request


class PostLoginBody:
    @property
    def email(self):
        return self.__email

    @property
    def password(self):
        return self.__password

    def __init__(self):
        data = request.get_json()
        self.__password = data.get("password")
        self.__email = data.get("email")
