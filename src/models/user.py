from pydantic import BaseModel
from pydantic import EmailStr

from pydantic_extra_types.phone_numbers import PhoneNumber


class UserBaseModel(BaseModel):
    """
    The user base model
    """

    name: str
    email: EmailStr
    phone: PhoneNumber


class User(UserBaseModel):
    id: str
