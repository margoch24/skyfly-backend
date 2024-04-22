from flask_restful import Resource

from api.helpers.request_validator import RequestValidatorTypes
from api.middlewares.validate_request import validate_request
from api.requests import PostContactUsBody
from api.schemas import PostContactUsSchema
from api.services.contact_us_service import ContactUsService


class ContactUsResource(Resource):

    @validate_request(PostContactUsSchema, RequestValidatorTypes.Body)
    def post(self):
        body = PostContactUsBody()

        response = ContactUsService.create_contact_us(
            body.name, body.email, body.phone_number, body.message
        )
        return response
