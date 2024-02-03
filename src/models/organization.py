from pydantic import BaseModel, EmailStr


class OrganizationBaseModel(BaseModel):
    name: str
    email: EmailStr
    logo_url: str = ""


class OrganizationSignUp(OrganizationBaseModel):
    password: str


class Organization(OrganizationBaseModel):
    org_id: str
    is_verified: bool
    date_created: str
