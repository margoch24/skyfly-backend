from api.controllers.contact_us_controller import ContactUsResource
from api.flask_app import FlaskApp

app = FlaskApp()

contact_us_blueprint = app.create_blueprint("contact_us")
contact_us_api = app.create_api(contact_us_blueprint)

app.add_resource(contact_us_api, ContactUsResource, "/contact_us")
