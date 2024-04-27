from marshmallow import Schema, fields


class GetFutureTicketsSchema(Schema):
    page = fields.Integer()
    limit = fields.Integer()
