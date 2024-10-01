from pydantic import BaseModel, EmailStr


class Invitation(BaseModel):
    """
    This would handle storing the data for an invitation.
    It handles everything in the invitation table.
    """

    user_email: EmailStr  # The email of the user that was invited.
    org_id: str  # The id of the org that invited this user
    date_invited: str
    date_accepted: str
    accepted: bool
