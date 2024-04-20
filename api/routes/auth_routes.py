from controllers.auth_controller import Login
from flask_app import FlaskApp

app = FlaskApp()

auth_blueprint = app.create_blueprint("auth")
auth_api = app.create_api(auth_blueprint)

app.add_resource(auth_api, Login, "/login")
