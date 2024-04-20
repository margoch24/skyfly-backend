from datetime import datetime, timezone

from flask import Response

from config import JWTConfig


def set_cookie(response: Response, key, value, expires_delta):
    expiration_time = datetime.now(timezone.utc) + expires_delta

    response.set_cookie(
        key,
        value,
        httponly=True,
        secure=JWTConfig.JWT_COOKIE_SECURE,
        expires=expiration_time,
    )
