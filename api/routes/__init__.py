from api.routes.auth_routes import auth_blueprint
from api.routes.contact_us_routes import contact_us_blueprint
from api.routes.flights_routes import flights_blueprint
from api.routes.images_routes import images_blueprint
from api.routes.reviews_routes import reviews_blueprint
from api.routes.tickets_routes import tickets_blueprint
from api.routes.user_routes import user_blueprint

__all__ = [
    auth_blueprint,
    contact_us_blueprint,
    flights_blueprint,
    reviews_blueprint,
    tickets_blueprint,
    images_blueprint,
    user_blueprint,
]
