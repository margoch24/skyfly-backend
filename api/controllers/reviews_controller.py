from flask_jwt_extended import jwt_required
from flask_restful import Resource

from api.helpers.request_validator import RequestValidatorTypes
from api.middlewares.validate_request import validate_request
from api.requests import PostReviewBody
from api.schemas import PostReviewSchema
from api.services.reviews_service import ReviewsService


class ReviewResource(Resource):

    @jwt_required()
    @validate_request(PostReviewSchema, RequestValidatorTypes.Body)
    def post(self):
        body = PostReviewBody()

        response = ReviewsService.create_review(body.message, body.rating)
        return response


class ReviewsResource(Resource):
    def get(self):
        response = ReviewsService.get_reviews()
        return response
