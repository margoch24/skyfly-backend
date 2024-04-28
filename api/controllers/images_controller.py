from flask import send_from_directory
from flask_restful import Resource

from api.helpers.request_validator import RequestValidatorTypes
from api.middlewares.validate_request import validate_request
from api.requests import GetImageQuery, UploadImageFiles
from api.schemas import GetImageSchema, UploadImageSchema
from api.services.images_service import ImagesService
from config import DefaultConfig


class GetImageResource(Resource):

    @validate_request(GetImageSchema, RequestValidatorTypes.Query)
    def get(self):
        query = GetImageQuery()

        response = send_from_directory(
            f"../{DefaultConfig.UPLOAD_FOLDER}", query.filename
        )
        response.headers["Cross-Origin-Resource-Policy"] = "*"
        return response


class UploadImageResource(Resource):

    @validate_request(UploadImageSchema, RequestValidatorTypes.Files)
    def post(self):
        files = UploadImageFiles()

        response = ImagesService.upload_image(files.file)
        return response
