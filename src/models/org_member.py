from enum import Enum

from pydantic import BaseModel


class MemberRole(str, Enum):
    """
    Handles the role of the members in the org

    Possible roles are 
    1. admin: can assign tasks

    """

    admin = "admin"

    pass


class OrgMember(BaseModel):
    user_id: str
    org_id: str
    date_joined: str
