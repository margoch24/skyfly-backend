from flask_jwt_extended import jwt_required
from flask_restful import Resource

from api.services.user_service import UserService


class UserResource(Resource):

    @jwt_required()
    def get(self):
        response = UserService.get_user()
        return response
