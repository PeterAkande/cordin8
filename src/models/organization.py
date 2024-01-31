from pydantic import BaseModel, EmailStr


class OrganizationBaseModel(BaseModel):
    name: str
    email: str
    logo_url: str = ""


class OrganizationSignUp(OrganizationBaseModel):
    password: str


class Organization:
    id: str
