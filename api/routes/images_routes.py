from api.controllers.images_controller import GetImageResource, UploadImageResource
from api.flask_app import FlaskApp

app = FlaskApp()

images_blueprint = app.create_blueprint("images")
images_api = app.create_api(images_blueprint)

app.add_resource(images_api, GetImageResource, "/image")
app.add_resource(images_api, UploadImageResource, "/upload-image")
