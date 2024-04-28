from api.schemas.auth.post_login_schema import PostLoginSchema
from api.schemas.auth.post_register_schema import PostRegisterSchema
from api.schemas.contact_us.post_contact_us_schema import PostContactUsSchema
from api.schemas.flights.get_flight_schema import GetFlightSchema
from api.schemas.flights.get_flights_schema import GetFlightsSchema
from api.schemas.flights.post_flight_schema import PostFlightSchema
from api.schemas.images.get_image_schema import GetImageSchema
from api.schemas.images.upload_image_schema import UploadImageSchema
from api.schemas.reviews.post_review_schema import PostReviewSchema
from api.schemas.tickets.get_future_tickets_schema import GetFutureTicketsSchema
from api.schemas.tickets.get_past_tickets_schema import GetPastTicketsSchema
from api.schemas.tickets.post_ticket_schema import PostTicketSchema

__all__ = [
    PostLoginSchema,
    PostRegisterSchema,
    PostReviewSchema,
    PostContactUsSchema,
    GetFlightSchema,
    PostFlightSchema,
    GetFlightsSchema,
    PostTicketSchema,
    GetPastTicketsSchema,
    GetFutureTicketsSchema,
    GetImageSchema,
    UploadImageSchema,
]
