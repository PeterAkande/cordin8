from marshmallow import Schema, fields


class UserBaseModel:
    name: fields.Str()
    email: fields.Email()
    phone: fields.Str()


class UserSignUp(UserBaseModel):
    """
    The user base model
    """

    password: fields.Str()


class User(UserBaseModel):
    id: fields.Str()
    date_created = fields.Date()
