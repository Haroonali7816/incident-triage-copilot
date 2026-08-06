from database import SessionLocal
from models import Incident
from embeddings import embed_text, incident_to_embedding_text
from vector_store import upsert_incident_embedding
 


def build_vector_index() -> None:
    db = SessionLocal()
    try:
        incidents = db.query(Incident).all()
    finally:
        db.close()

    print(f"Embedding {len(incidents)} incidents locally...")

    for i, incident in enumerate(incidents,start=1):
        text = incident_to_embedding_text(incident.title,incident.body)
        embedding = embed_text(text)
        upsert_incident_embedding(incident.id,embedding)

        if i % 50 == 0 or i == len(incidents):
            print(f" {i}/{len(incidents)} embedded")

    print("Done")


if __name__ == "__main__":
    build_vector_index()