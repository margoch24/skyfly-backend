from api.controllers.flights_controller import FlightResource, FlightsResource
from api.flask_app import FlaskApp

app = FlaskApp()

flights_blueprint = app.create_blueprint("flights")
flights_api = app.create_api(flights_blueprint)

app.add_resource(flights_api, FlightResource, "/flight")
app.add_resource(flights_api, FlightsResource, "/flights")
