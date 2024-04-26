from marshmallow import Schema, fields


class PostContactUsSchema(Schema):
    message = fields.Str(required=True)
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    phone_number = fields.Str(required=True)
