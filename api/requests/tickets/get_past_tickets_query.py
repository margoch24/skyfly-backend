from flask import request


class GetPastTicketsQuery:

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
        self.__page = data.get("page")
        self.__limit = data.get("limit")
