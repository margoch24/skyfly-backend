from flask_jwt_extended import jwt_required
from flask_restful import Resource

from api.helpers.request_validator import RequestValidatorTypes
from api.middlewares.validate_request import validate_request
from api.requests import (
    GetCheckTicketQuery,
    GetFutureTicketsQuery,
    GetPastTicketsQuery,
    PostTicketBody,
)
from api.schemas import (
    GetCheckTicketSchema,
    GetFutureTicketsSchema,
    GetPastTicketsSchema,
    PostTicketSchema,
)
from api.services.tickets_service import TicketsService


class TicketResource(Resource):

    @jwt_required()
    @validate_request(PostTicketSchema, RequestValidatorTypes.Body)
    def post(self):
        body = PostTicketBody()

        response = TicketsService.create_ticket(
            body.name, body.surname, body.date_of_birth, body.flight_id, body.seat_id
        )
        return response


class PastTicketsResource(Resource):

    @jwt_required()
    @validate_request(GetPastTicketsSchema, RequestValidatorTypes.Query)
    def get(self):
        query = GetPastTicketsQuery()

        response = TicketsService.get_tickets(query.limit, query.page, "past")
        return response


class FutureTicketsResource(Resource):

    @jwt_required()
    @validate_request(GetFutureTicketsSchema, RequestValidatorTypes.Query)
    def get(self):
        query = GetFutureTicketsQuery()

        response = TicketsService.get_tickets(query.limit, query.page, "future")
        return response


class CheckTicketResource(Resource):

    @jwt_required()
    @validate_request(GetCheckTicketSchema, RequestValidatorTypes.Query)
    def get(self):
        query = GetCheckTicketQuery()

        response = TicketsService.check_ticket(query.ticket_id)
        return response
