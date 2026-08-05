import logging
import time

from database import SessionLocal
from models import Incident
from classifier import classify_incident

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("classify_pending")

SECONDS_BETWEEN_REQUESTS = 5


def classify_pending_incidents(limit: int | None = None) -> None:
    db = SessionLocal()
    succeeded = 0
    failed = 0

    try:
        query = db.query(Incident).filter(Incident.severity.is_(None))
        if limit is not None:
            query = query.limit(limit)
        pending = query.all()

        logger.info(f"Found {len(pending)} unclassified incidents")

        for incident in pending:
            try:
                result = classify_incident(incident.title, incident.body)
                incident.severity = result.severity
                incident.category = result.category
                incident.summary = result.summary
                db.commit()
                succeeded += 1
                logger.info(
                    f"#{incident.github_number}: {result.severity}/{result.category}"
                )
            except Exception as e:
                # Graceful degradation: one bad issue must not kill the whole batch.
                # We log it, roll back just this incident's uncommitted change,
                # and move on to the next one.
                db.rollback()
                failed += 1
                logger.error(
                    f"#{incident.github_number}: classification failed after "
                    f"retries -> {type(e).__name__}: {e}"
                )

            time.sleep(SECONDS_BETWEEN_REQUESTS)

    finally:
        db.close()

    logger.info(f"Done. Succeeded: {succeeded}, Failed: {failed}")


if __name__ == "__main__":
    classify_pending_incidents()