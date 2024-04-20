class ServiceResponse:

    @property
    def status(self):
        return self.__status

    @property
    def response(self):
        return self.__response

    def __init__(self, status, response):
        self.__status = status
        self.__response = response
