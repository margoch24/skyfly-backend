from flask_jwt_extended import JWTManager, decode_token

from api.helpers.jwt import jwt_cases_handling, jwt_errors_handling


class FlaskJWT:

    def __init__(self):
        self.__jwt = JWTManager()

    def initiate(self, app):
        self.__jwt = JWTManager(app)
        self.errors_handling()
        self.cases_handling()

    def errors_handling(self):
        jwt = self.__jwt
        jwt_errors_handling(jwt)

    def cases_handling(self):
        jwt = self.__jwt
        jwt_cases_handling(jwt)

    def decode_token(self, token):
        try:
            decoded_token = decode_token(token)
            decoded_token["is_valid"] = True
        except:
            decoded_token = {
                "is_valid": False,
                "error_response": {
                    "error": 1,
                    "data": {"message": "Signature verification failed"},
                },
            }

        return decoded_token
