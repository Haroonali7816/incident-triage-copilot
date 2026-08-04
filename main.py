from fastapi import  Depends, FastAPI , HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Incident
from schemas import IncidentRead

app = FastAPI(title="Incident Triage Copilot")


@app.get("/incidents", response_model=list[IncidentRead])
def list_incidents(
    skip: int = 0,
    limit: int = 20,
    severity: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Incident)
    if severity is not None:
        query = query.filter(Incident.severity == severity)
    return query.offset(skip).limit(limit).all()

@app.get("/incidents/{incident_id}", response_model=IncidentRead)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident