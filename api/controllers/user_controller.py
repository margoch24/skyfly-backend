from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from api.helpers.request_validator import RequestValidatorTypes
from api.middlewares.validate_request import validate_request
from api.requests import PutUserBody
from api.schemas import PutUserSchema
from api.services.user_service import UserService


class UserResource(Resource):

    @jwt_required()
    def get(self):
        isAdmin = request.headers.get("referrer-type") == "admin"
        response = UserService.get_user(isAdmin)
        return response

    @jwt_required()
    @validate_request(PutUserSchema, RequestValidatorTypes.Body)
    def put(self):
        body = PutUserBody()

        response = UserService.update_user(body.name, body.phone_number, body.photo)
        return response
