from api.schemas.auth.post_login_schema import PostLoginSchema
from api.schemas.auth.post_register_schema import PostRegisterSchema
from api.schemas.contact_us.post_contact_us_schema import PostContactUsSchema
from api.schemas.flights.get_flight_schema import GetFlightSchema
from api.schemas.flights.get_flights_schema import GetFlightsSchema
from api.schemas.flights.post_flight_schema import PostFlightSchema
from api.schemas.reviews.post_review_schema import PostReviewSchema

__all__ = [
    PostLoginSchema,
    PostRegisterSchema,
    PostReviewSchema,
    PostContactUsSchema,
    GetFlightSchema,
    PostFlightSchema,
    GetFlightsSchema,
]
