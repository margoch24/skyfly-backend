from marshmallow import Schema, fields


class GetPastTicketsSchema(Schema):
    page = fields.Integer()
    limit = fields.Integer()
