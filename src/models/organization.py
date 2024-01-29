from pydantic import BaseModel, EmailStr


class OrganizationBaseModel(BaseModel):
    name: str
    email: EmailStr
    logo_url: str = ""


class Organization(BaseModel):
    id: str
