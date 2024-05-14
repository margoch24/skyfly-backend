from flask_jwt_extended import jwt_required
from flask_restful import Resource

from api.helpers.request_validator import RequestValidatorTypes
from api.middlewares.validate_request import validate_request
from api.requests import GetFlightQuery, GetFlightsQuery, PostFlightBody
from api.schemas import GetFlightSchema, GetFlightsSchema, PostFlightSchema
from api.services.flights_service import FlightsService


class FlightResource(Resource):

    @jwt_required()
    @validate_request(PostFlightSchema, RequestValidatorTypes.Body)
    def post(self):
        body = PostFlightBody()

        response = FlightsService.create_flight(
            body.arrival,
            body.airline,
            body.cabin_class,
            body.departure,
            body.photo,
            body.score,
            body.scheduled,
            body.price,
            body.currency,
            body.from_latitude,
            body.from_longitude,
            body.to_latitude,
            body.to_longitude,
        )
        return response

    @validate_request(GetFlightSchema, RequestValidatorTypes.Query)
    def get(self):
        query = GetFlightQuery()

        response = FlightsService.get_flight(flight_id=query.flight_id)
        return response


class FlightsResource(Resource):

    @validate_request(GetFlightsSchema, RequestValidatorTypes.Query)
    def get(self):
        query = GetFlightsQuery()

        response = FlightsService.get_flights(
            query.arrival,
            query.cabin_class,
            query.departure,
            query.page,
            query.price,
            query.limit,
            query.from_latitude,
            query.from_longitude,
            query.to_latitude,
            query.to_longitude,
        )
        return response
