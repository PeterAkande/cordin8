from pydantic import BaseModel


class Department(BaseModel):
    name: str
    team_lead: str  # This would be the ID Of the Team Lead.
