from marshmallow import Schema, fields

from api.helpers.validation import cabin_class_validation, price_range_validation


class GetFlightsSchema(Schema):
    from_longitude = fields.Float()
    from_latitude = fields.Float()
    to_longitude = fields.Float()
    to_latitude = fields.Float()
    departure = fields.Integer()
    arrival = fields.Integer()
    cabin_class = fields.String(validate=cabin_class_validation)
    price = fields.String(validate=price_range_validation)
    page = fields.Integer()
    limit = fields.Integer()
