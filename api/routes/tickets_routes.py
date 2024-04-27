from api.controllers.tickets_controller import (
    FutureTicketsResource,
    PastTicketsResource,
    TicketResource,
)
from api.flask_app import FlaskApp

app = FlaskApp()

tickets_blueprint = app.create_blueprint("tickets")
tickets_api = app.create_api(tickets_blueprint)

app.add_resource(tickets_api, TicketResource, "/ticket")
app.add_resource(tickets_api, FutureTicketsResource, "/future-tickets")
app.add_resource(tickets_api, PastTicketsResource, "/past-tickets")
