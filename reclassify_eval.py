import json
import time

from database import SessionLocal
from models import Incident
from classifier import classify_incident

LLM_PREDICTIONS_V1_PATH = "eval/llm_predictions.json"
LLM_PREDICTIONS_V2_PATH = "eval/llm_predictions_v2.json"
SECONDS_BETWEEN_REQUESTS = 5


def reclassify_eval_sample() -> None:
    with open(LLM_PREDICTIONS_V1_PATH, "r", encoding="utf-8") as f:
        v1_predictions = json.load(f)

    github_numbers = [int(n) for n in v1_predictions.keys()]

    db = SessionLocal()
    try:
        incidents = (
            db.query(Incident)
            .filter(Incident.github_number.in_(github_numbers))
            .all()
        )
    finally:
        db.close()

    print(f"Re-classifying {len(incidents)} eval-sample incidents with the revised prompt...")

    v2_predictions = {}
    for incident in incidents:
        try:
            result = classify_incident(incident.title, incident.body)
            v2_predictions[str(incident.github_number)] = {
                "severity": result.severity,
                "category": result.category,
                "summary": result.summary,
            }
            print(f"#{incident.github_number}: {result.severity}/{result.category}")
        except Exception as e:
            print(f"#{incident.github_number}: failed -> {type(e).__name__}: {e}")

        time.sleep(SECONDS_BETWEEN_REQUESTS)

    with open(LLM_PREDICTIONS_V2_PATH, "w", encoding="utf-8") as f:
        json.dump(v2_predictions, f, indent=2)

    print(f"Wrote {len(v2_predictions)} v2 predictions to {LLM_PREDICTIONS_V2_PATH}")


if __name__ == "__main__":
    reclassify_eval_sample()