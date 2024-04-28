from marshmallow import Schema, fields


class GetCheckTicketSchema(Schema):
    ticket_id = fields.UUID(required=True)
