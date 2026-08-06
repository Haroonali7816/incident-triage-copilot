from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Incident
from schemas import IncidentRead, SimilarIncident
from embeddings import embed_text, incident_to_embedding_text
from vector_store import get_embedding, upsert_incident_embedding, query_similar

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


@app.get("/incidents/{incident_id}/similar", response_model=list[SimilarIncident])
def get_similar_incidents(incident_id: int, top_k: int = 5, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")

    embedding = get_embedding(incident.id)
    if embedding is None:
        # Lazily embed on first request if the batch index hasn't covered
        # this incident yet (e.g. added after the last build_vector_index.py
        # run), rather than erroring.
        text = incident_to_embedding_text(incident.title, incident.body)
        embedding = embed_text(text)
        upsert_incident_embedding(incident.id, embedding)

    similar = query_similar(embedding, top_k=top_k, exclude_id=incident.id)

    results = []
    for similar_id, score in similar:
        similar_incident = db.query(Incident).filter(Incident.id == similar_id).first()
        if similar_incident is not None:
            # Build the ORM-derived fields first (title, severity, etc. --
            # everything similarity_score is NOT), then combine with the
            # score in one construction step. Calling SimilarIncident.model_validate()
            # directly on the ORM object fails validation immediately, since
            # similarity_score is a required field that doesn't exist on the
            # database row at all -- it only exists from the vector search.
            base_fields = IncidentRead.model_validate(similar_incident).model_dump()
            result = SimilarIncident(**base_fields, similarity_score=score)
            results.append(result)

    return results