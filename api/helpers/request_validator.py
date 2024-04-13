from abc import ABC, abstractmethod

from flask import request
from marshmallow import Schema


class RequestValidatorTypes:
    Body = "body"
    Query = "query"


class RequestValidator(ABC):
    def __init__(self, schema: Schema):
        self._schema = schema
        self._errors = None

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def load(self):
        pass


class BodyRequestValidator(RequestValidator):
    def validate(self):
        self._errors = self._schema.validate(request.json)
        return self._errors

    def load(self):
        return self._schema.load(request.json)


class QueryRequestValidator(RequestValidator):
    def validate(self):
        self._errors = self._schema.validate(request.args)
        return self._errors

    def load(self):
        return self._schema.load(request.args)
