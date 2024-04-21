from flask import request


class PostReviewBody:

    @property
    def message(self):
        return self.__message

    @property
    def rating(self):
        return self.__rating

    def __init__(self):
        data = request.get_json()
        self.__message = data.get("message")
        self.__rating = data.get("rating")
