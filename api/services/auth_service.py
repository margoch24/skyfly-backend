from datetime import timedelta

from flask import make_response, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt

from api.bcrypt_flask import FlaskBcrypt
from api.helpers.cookies import set_cookie
from api.jwt_flask import FlaskJWT
from api.models import Admin, TokenBlocklist, User
from config import JWTConfig

bcrypt = FlaskBcrypt()
flask_jwt = FlaskJWT()


class AuthService:

    def post_login(email: str, password: str, isAdmin):
        return login(email, password, isAdmin)

    def post_register(email: str, password: str, name: str, phone_number: str):
        return register(email, password, name, phone_number)

    def post_refresh_access():
        return refresh_access()

    def post_logout():
        return logout()


def login(email: str, password: str, isAdmin):
    try:
        if isAdmin:
            user = Admin.find_one({"email": email, "is_deleted": False})
        else:
            user = User.find_one({"email": email, "is_deleted": False})

        if not user:
            response = {"error": 1, "data": {"message": "Account does not exist"}}
            return response, 403

        isValidPassword = bcrypt.check_password(user.password, password)
        if not isValidPassword:
            response = {
                "error": 1,
                "data": {"message": "Invalid password information entered"},
            }
            return response, 403

        access_token = create_access_token(
            identity=user.id, expires_delta=JWTConfig.JWT_ACCESS_TOKEN_EXPIRATION
        )
        refresh_token = create_refresh_token(
            identity=user.id, expires_delta=JWTConfig.JWT_REFRESH_TOKEN_EXPIRATION
        )

        if isAdmin:
            updated_user = Admin.update_one(
                record_id=user.id, refresh_token=refresh_token
            )
        else:
            updated_user = User.update_one(
                record_id=user.id, refresh_token=refresh_token
            )

        if not updated_user:
            raise Exception("Unable to update user info")
    except Exception as e:
        print(f"ERROR (login): {e}")

        response = {"error": 1, "data": {"message": "Internal server error"}}
        return response, 500

    response_data = {
        "error": 0,
        "data": {"access_token": access_token},
    }

    response = make_response(response_data, 200)
    set_cookie(
        response,
        "refresh_token",
        refresh_token,
        expires_delta=JWTConfig.JWT_REFRESH_TOKEN_EXPIRATION,
    )
    return response


def register(email: str, password: str, name: str, phone_number: str):
    try:
        user_exists = User.find_one({"email": email, "is_deleted": False})
        if user_exists:
            response = {"error": 1, "data": {"message": "Account already exists"}}
            return response, 409

        hashed_password = bcrypt.hash_password(password)
        user = User.create(
            email=email, password=hashed_password, name=name, phone_number=phone_number
        )
    except Exception as e:
        print(f"ERROR (register): {e}")

        response = {"error": 1, "data": {"message": "Internal server error"}}
        return response, 500

    response = {
        "error": 0,
        "data": user.serialize(),
    }
    return response, 200


def refresh_access():
    try:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            return {"error": 1, "data": {"message": "Refresh token is missing"}}, 401

        decoded_token = flask_jwt.decode_token(refresh_token)
        if not decoded_token["is_valid"]:
            return decoded_token["error_response"], 401

        user_id = decoded_token["sub"]

        user = User.find_one({"id": user_id, "is_deleted": False})
        if not user:
            response = {"error": 1, "data": {"message": "Insufficient permissions"}}
            return response, 403

        new_access_token = create_access_token(
            identity=user_id, expires_delta=JWTConfig.JWT_ACCESS_TOKEN_EXPIRATION
        )
    except Exception as e:
        print(f"ERROR (refresh_access): {e}")

        response = {"error": 1, "data": {"message": "Internal server error"}}
        return response, 500

    response = {
        "error": 0,
        "data": {"access_token": new_access_token},
    }
    return response, 200


def logout():
    try:
        refresh_token = request.cookies.get("refresh_token")
        if refresh_token:
            decoded_token = flask_jwt.decode_token(refresh_token)
            if not decoded_token["is_valid"]:
                return decoded_token["error_response"], 401

            decoded_jti = decoded_token["jti"]
            decoded_type = decoded_token["type"]
            TokenBlocklist.create(jti=decoded_jti, type=decoded_type)

        access_token = get_jwt()
        access_jti = access_token["jti"]
        access_type = access_token["type"]

        TokenBlocklist.create(jti=access_jti, type=access_type)
    except Exception as e:
        print(f"ERROR (logout): {e}")

        response = {"error": 1, "data": {"message": "Internal server error"}}
        return response, 500

    response = make_response({"error": 0})
    set_cookie(response, "refresh_token", "", expires_delta=timedelta(days=3))
    return response
