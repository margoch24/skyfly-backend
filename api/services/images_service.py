import os

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from api.helpers import get_random
from api.helpers.images import allowed_file
from config import DefaultConfig


class ImagesService:

    def upload_image(file: FileStorage):
        return upload_image(file)


def upload_image(file: FileStorage):
    if file.filename == "":
        response = {"error": 1, "data": {"message": "No selected file"}}
        return response, 400

    try:
        if not allowed_file(file.filename):
            response = {"error": 1, "data": {"message": "Invalid file type"}}
            return response, 400

        current_dir = os.path.dirname(os.path.abspath(__file__))

        uploads_dir = os.path.join(current_dir, f"../../{DefaultConfig.UPLOAD_FOLDER}/")

        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)

        secured_filename = secure_filename(file.filename)
        filename = f"{get_random(100000)}_{secured_filename}"
        file.save(os.path.join(uploads_dir, filename))

    except Exception as e:
        print(f"ERROR (upload_image): {e}")

        response = {"error": 1, "data": {"message": "Internal server error"}}
        return response, 500

    response = {"error": 0, "data": {"filename": filename}}
    return response, 200
