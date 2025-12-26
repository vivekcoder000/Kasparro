from sqlalchemy import text

def get_etl_stats(db):
    total_runs = db.execute(
        text("SELECT COUNT(*) FROM etl_runs")
    ).scalar()

    last_success = db.execute(
        text("""
            SELECT finished_at
            FROM etl_runs
            WHERE status = 'success'
            ORDER BY finished_at DESC
            LIMIT 1
        """)
    ).scalar()

    last_failure = db.execute(
        text("""
            SELECT finished_at
            FROM etl_runs
            WHERE status = 'failed'
            ORDER BY finished_at DESC
            LIMIT 1
        """)
    ).scalar()

    last_run = db.execute(
        text("""
            SELECT status, started_at, finished_at
            FROM etl_runs
            ORDER BY started_at DESC
            LIMIT 1
        """)
    ).fetchone()

    duration = None
    if last_run and last_run.finished_at and last_run.started_at:
        duration = (
            last_run.finished_at - last_run.started_at
        ).total_seconds()

    return {
        "total_runs": total_runs,
        "last_success": last_success,
        "last_failure": last_failure,
        "last_run_status": last_run.status if last_run else None,
        "last_run_duration_sec": duration
    }
