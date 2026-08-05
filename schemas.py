from datetime import datetime
from pydantic import BaseModel, ConfigDict

class IncidentBase(BaseModel):
    github_id: int
    github_number: int
    html_url:str
    title: str
    body: str | None = None
    state: str
    labels: list[str] = []
    created_at: datetime
    closed_at: datetime | None = None


class IncidentCreate(IncidentBase):
    pass

class IncidentRead(IncidentBase):
    model_config = ConfigDict(from_attributes=True)  # lets this read straight from an ORM object

    id: int
    severity: str | None = None
    category: str | None = None
    summary: str | None = None