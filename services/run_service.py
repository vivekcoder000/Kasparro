from core.db import SessionLocal
from schemas.models import ETLRun
from datetime import datetime

def start_etl_run():
    db = SessionLocal()
    try:
        run = ETLRun(
            started_at=datetime.utcnow(),
            status="running",
            records_processed=0
        )
        db.add(run)
        db.commit()
        db.refresh(run)
        return run.id
    finally:
        db.close()

def mark_run_success(run_id, records_processed=0):
    db = SessionLocal()
    try:
        run = db.query(ETLRun).get(run_id)
        if run:
            run.finished_at = datetime.utcnow()
            run.status = "success"
            run.records_processed = records_processed
            db.commit()
    finally:
        db.close()

def mark_run_failure(run_id, error_message):
    db = SessionLocal()
    try:
        run = db.query(ETLRun).get(run_id)
        if run:
            run.finished_at = datetime.utcnow()
            run.status = "failed"
            # run.error = error_message # If we have an error column
            db.commit()
    finally:
        db.close()
