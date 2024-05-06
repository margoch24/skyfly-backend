from flask_jwt_extended import get_jwt_identity

from api.models import Admin, User


class UserService:

    def get_user(isAdmin):
        return get_user(isAdmin)

    def update_user(name: str, phone_number: str, photo: str):
        return update_user(name, phone_number, photo)


def get_user(isAdmin):
    try:
        user_id = get_jwt_identity()
        if isAdmin:
            user: Admin = Admin.find_one({"id": user_id, "is_deleted": False})
        else:
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


def update_user(name: str, phone_number: str, photo: str):
    try:
        user_id = get_jwt_identity()
        user_exist = User.find_one({"id": user_id, "is_deleted": False})

        if not user_exist:
            response = {"error": 1, "data": {"message": "Insufficient permissions"}}
            return response, 403

        update_params = {"name": name, "phone_number": phone_number, "photo": photo}
        valid_update_params = {
            key: value for key, value in update_params.items() if value
        }

        User.update_one(user_exist.id, **valid_update_params)

    except Exception as e:
        print(f"ERROR (update_user): {e}")

        response = {"error": 1, "data": {"message": "Internal server error"}}
        return response, 500

    response = {"error": 0}
    return response, 200
