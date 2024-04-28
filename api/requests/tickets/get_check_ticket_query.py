from flask import request


class GetCheckTicketQuery:
    @property
    def ticket_id(self):
        return self.__ticket_id

    def __init__(self):
        data = request.args
        self.__ticket_id = data.get("ticket_id")
