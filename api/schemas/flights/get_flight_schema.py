from marshmallow import Schema, fields


class GetFlightSchema(Schema):
    flight_id = fields.UUID(required=True)
