from marshmallow import Schema, fields


class PostLoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)
