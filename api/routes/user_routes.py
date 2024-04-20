from api.controllers.user_controller import UserResource
from api.flask_app import FlaskApp

app = FlaskApp()

user_blueprint = app.create_blueprint("user")
user_api = app.create_api(user_blueprint)

app.add_resource(user_api, UserResource, "/user")
