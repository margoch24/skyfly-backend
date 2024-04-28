from flask import request


class GetImageQuery:
    @property
    def filename(self):
        return self.__filename

    def __init__(self):
        data = request.args
        self.__filename = data.get("filename")
