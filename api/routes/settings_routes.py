from api.controllers.settings_controller import DiscountsResource
from api.flask_app import FlaskApp

app = FlaskApp()

settings_blueprint = app.create_blueprint("settings")
settings_api = app.create_api(settings_blueprint)

app.add_resource(settings_api, DiscountsResource, "/discounts")
