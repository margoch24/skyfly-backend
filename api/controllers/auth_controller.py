from flask_restful import Resource
from helpers.request_validator import RequestValidatorTypes
from middlewares.validate_request import validate_request
from schemas import PostLoginSchema
from services.auth_service import AuthService

from api.requests import PostLoginBody


class Login(Resource):

    @validate_request(PostLoginSchema, RequestValidatorTypes.Body)
    def post(self):
        body = PostLoginBody()
        res = AuthService.post_login(body.email, body.password)
        return res.response, res.status
