from pydantic import BaseModel, EmailStr

from pydantic_extra_types.phone_numbers import PhoneNumber


class UserBaseModel(BaseModel):
    name: str
    email: EmailStr
    phone: PhoneNumber


class UserSignUp(UserBaseModel):
    """
    The user base model
    """

    password: str


class User(UserBaseModel):
    user_id: str
    date_created: str
    isVerified: bool
