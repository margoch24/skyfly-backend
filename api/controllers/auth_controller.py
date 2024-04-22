from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from api.helpers.request_validator import RequestValidatorTypes
from api.middlewares.validate_request import validate_request
from api.requests import PostLoginBody, PostRegisterBody
from api.schemas import PostLoginSchema, PostRegisterSchema
from api.services.auth_service import AuthService


class LoginResource(Resource):

    @validate_request(PostLoginSchema, RequestValidatorTypes.Body)
    def post(self):
        isAdmin = request.headers.get("referrer-type") == "admin"
        body = PostLoginBody()

        response = AuthService.post_login(body.email, body.password, isAdmin)
        return response


class RegisterResource(Resource):

    @validate_request(PostRegisterSchema, RequestValidatorTypes.Body)
    def post(self):
        body = PostRegisterBody()
        response = AuthService.post_register(
            body.email, body.password, body.name, body.phone_number
        )
        return response


class RefreshAccessResource(Resource):

    def post(self):
        response = AuthService.post_refresh_access()
        return response


class LogoutResource(Resource):

    @jwt_required()
    def post(self):
        response = AuthService.post_logout()
        return response
