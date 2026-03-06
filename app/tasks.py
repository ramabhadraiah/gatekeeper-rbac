import time
from datetime import datetime, timezone

from app.celery_app import celery_app


@celery_app.task(name="execute_job")
def run_job(payload: dict) -> dict:
    time.sleep(1)
    return {"echo": payload, "processed_at": datetime.now(timezone.utc).isoformat()}

