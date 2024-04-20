from flask_jwt_extended import JWTManager


def jwt_errors_handling(jwt: JWTManager):
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return {
            "error": 1,
            "data": {"message": "Token has expired"},
        }, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {
            "error": 1,
            "data": {"message": "Signature verification failed"},
        }, 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {
            "error": 1,
            "data": {"message": "Request doesn't contain valid token"},
        }, 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_data):
        return {
            "error": 1,
            "data": {"message": "Token has been revoked"},
        }, 401


def jwt_cases_handling(jwt: JWTManager):
    from api.models import TokenBlocklist

    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(jwt_header, jwt_data):
        jti = jwt_data["jti"]
        token = TokenBlocklist.find_one({"jti": jti})

        return token is not None
