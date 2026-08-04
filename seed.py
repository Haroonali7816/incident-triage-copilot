import json
from database import Base, engine, SessionLocal
from models import Incident
from transform import github_issue_to_incident_dict
from datetime import datetime

RAW_ISSUES_PATH = "data/raw_issues.json"

def seed():
    Base.metadata.create_all(bind=engine) # this will create a table if it doesn't exist yet.

    with open(RAW_ISSUES_PATH, "r", encoding= "utf-8") as f:
        raw_issues = json.load(f)

    db = SessionLocal()
    inserted = 0
    skipped =  0

    try:
        for raw in raw_issues:
            incident_data = github_issue_to_incident_dict(raw)

            # Check if the incident already exists in the database
            exists = (
                db.query(Incident)
                .filter(Incident.github_id == incident_data["github_id"])
                .first()
            )
            if exists:
                skipped += 1
                continue

            db.add(Incident(**incident_data))
            inserted += 1
        db.commit()
    finally:
        db.close()

    print(f"Seed complete: {inserted} inserted, {skipped} already existed")

if __name__ == "__main__":
    seed()