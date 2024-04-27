from marshmallow import Schema, fields, validate


class PostTicketSchema(Schema):
    name = fields.String(required=True)
    surname = fields.String(required=True)
    date_of_birth = fields.Integer(required=True)
    seat_id = fields.UUID(required=True)
    flight_id = fields.UUID(required=True)
