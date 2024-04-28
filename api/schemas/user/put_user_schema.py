from marshmallow import Schema, fields, validate


class PutUserSchema(Schema):
    name = fields.Str()
    phone_number = fields.Str()
    photo = fields.Str()
