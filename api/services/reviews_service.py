from flask_jwt_extended import get_jwt_identity

from api.models import Review, User


class ReviewsService:

    def get_reviews():
        return get_reviews()

    def create_review(message: str, rating: str):
        return create_review(message, rating)


def get_reviews():
    try:
        reviews = Review.find(
            order_by=[Review.created_at.desc()],
            join=[
                {"table": User, "condition": Review.user_id == User.id},
            ],
        )
    except Exception as e:
        print(f"ERROR (get_reviews): {e}")

        response = {"error": 1, "data": {"message": "Internal server error"}}
        return response, 500

    serialized_reviews = [
        {**review.serialize(), "user": review.user.serialize()} for review in reviews
    ]

    response = {
        "error": 0,
        "data": serialized_reviews,
    }
    return response, 200


def create_review(message: str, rating: str):
    try:
        user_id = get_jwt_identity()
        user_exist = User.find_one({"id": user_id, "is_deleted": False})

        if not user_exist:
            response = {"error": 1, "data": {"message": "Insufficient permissions"}}
            return response, 403

        review = Review.create(user_id=user_id, message=message, rating=rating)
    except Exception as e:
        print(f"ERROR (create_review): {e}")

    if not review:
        response = {"error": 1, "data": {"message": "Internal server error"}}
        return response, 500

    response = {
        "error": 0,
        "data": review.serialize(),
    }
    return response, 200
