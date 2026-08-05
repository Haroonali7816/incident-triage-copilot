import csv
import json
import os
import random

from database import SessionLocal
from models import Incident

SAMPLE_SIZE = 40
RANDOM_SEED = 42

LABELLING_SHEET_PATH = "eval/labelling_sheet.csv"
LLM_PREDICTIONS_PATH = "eval/llm_predictions.json"

def generate_eval_sample()-> None:
    db = SessionLocal()
    try:
        classified = db.query(Incident).filter(Incident.severity.isnot(None)).all()
    finally:
        db.close()
    if not classified:
        print("No classified incidents found yet.")
        return

    if len(classified) < SAMPLE_SIZE:
        print(
            f"Warning: only {len(classified)} classified incidents available,"
            f"sampling all of them instead of {SAMPLE_SIZE}"
        )
    random.seed(RANDOM_SEED)
    sample = random.sample(classified, min(SAMPLE_SIZE, len(classified)))

    os.makedirs("eval", exist_ok=True)

    # we are blind labeling sheet and deliberately not including LLM prediction's.
    # Seeing them first would anchor our judgement towards agreeing with thhe model.

    with open(LABELLING_SHEET_PATH, "w", newline= "", encoding= "utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "github_number",
                "html_url",
                "title",
                "body",
                "human_severity",
                "human_category",
                "notes",
            ]
        )
        for incident in sample:
            writer.writerow(
                [
                    incident.github_number,
                    incident.html_url,
                    incident.title,
                    (incident.body or "")[:2000],
                    "",
                    "",
                    "",
                ]
            )


        llm_predictions = {
            str(incident.github_number): {
                "severity" : incident.severity,
                "category" : incident.category,
                "summary" : incident.summary,
            }
            for incident in sample
        }
        with open(LLM_PREDICTIONS_PATH, "w", encoding= "utf-8") as f:
            json.dump(llm_predictions,f, indent=2 )

        print(f"Sampled {len(sample)} incidents.")
        print(f"-> Label these by hand in: {LABELLING_SHEET_PATH}")
        print(f"-> (LLM predictions kept hidden in {LLM_PREDICTIONS_PATH} until you've done labeling.)")


if __name__ == "__main__":
    generate_eval_sample()
