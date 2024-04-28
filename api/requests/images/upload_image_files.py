from flask import request


class UploadImageFiles:
    @property
    def file(self):
        return self.__file

    def __init__(self):
        data = request.files
        self.__file = data.get("file")
