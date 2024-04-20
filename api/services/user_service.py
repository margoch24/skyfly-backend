from flask_jwt_extended import get_jwt_identity

from api.models import User


class UserService:

    def get_user():
        return get_user()


def get_user():
    try:
        user_id = get_jwt_identity()
        user: User = User.find_one({"id": user_id, "is_deleted": False})

    except Exception as e:
        print(f"ERROR (get_user): {e}")

        response = {"error": 1, "data": {"message": "Internal server error"}}
        return response, 500

    if not user:
        response = {"error": 1, "data": {"message": "Insufficient permissions"}}
        return response, 403

    response = {
        "error": 0,
        "data": user.serialize(),
    }
    return response, 200
