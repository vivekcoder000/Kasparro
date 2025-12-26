from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from core.db import get_db

router = APIRouter()

@router.get("/health")
def health(db: Session = Depends(get_db)):
    db_status = "down"
    etl_status = "unknown"

    try:
        # Check DB connectivity
        db.execute(text("SELECT 1"))
        db_status = "up"

        # Check last ETL run status
        result = db.execute(
            text("""
                SELECT status
                FROM etl_runs
                ORDER BY started_at DESC
                LIMIT 1
            """)
        ).fetchone()

        if result:
            etl_status = result[0]

    except Exception:
        db_status = "down"

    return {
        "status": "ok",
        "database": db_status,
        "etl_last_run": etl_status
    }
