from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic import BaseModel, EmailStr


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
    is_verified: bool


if __name__ == "__main__":
    data = {
        "user_id": "8696bd7a-85e1-4c0d-8c41-85b8a1e8adcc",
        "email": "akandepeter86@gmail.com",
        "date_created": "2024-02-03T03:41:32.464498",
        "name": "Akande Peter",
        "phone": "tel:+234-906-992-5482",
        "is_verified": True,
    }

    user = User(**data)

    print(user)
