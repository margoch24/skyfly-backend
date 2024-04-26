from api.requests.auth.post_login_body import PostLoginBody
from api.requests.auth.post_register_body import PostRegisterBody
from api.requests.contact_us.post_contact_us_body import PostContactUsBody
from api.requests.flights.get_flight_query import GetFlightQuery
from api.requests.flights.get_flights_query import GetFlightsQuery
from api.requests.flights.post_flight_body import PostFlightBody
from api.requests.reviews.post_review_body import PostReviewBody

__all__ = [
    PostLoginBody,
    PostRegisterBody,
    PostReviewBody,
    PostContactUsBody,
    GetFlightQuery,
    PostFlightBody,
    GetFlightsQuery,
]
