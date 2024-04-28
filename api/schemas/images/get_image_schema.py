from marshmallow import Schema, fields


class GetImageSchema(Schema):
    filename = fields.String(required=True)
