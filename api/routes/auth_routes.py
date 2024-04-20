from api.controllers.auth_controller import (
    LoginResource,
    LogoutResource,
    RefreshAccessResource,
    RegisterResource,
)
from api.flask_app import FlaskApp

app = FlaskApp()

auth_blueprint = app.create_blueprint("auth")
auth_api = app.create_api(auth_blueprint)

app.add_resource(auth_api, LoginResource, "/login")
app.add_resource(auth_api, RegisterResource, "/register")
app.add_resource(auth_api, RefreshAccessResource, "/refresh-access")
app.add_resource(auth_api, LogoutResource, "/logout")
