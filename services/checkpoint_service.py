from sqlalchemy import text

# Checkpoints track last successfully processed record/index
# to guarantee idempotent ETL runs and avoid re-processing data.
def get_checkpoint(db, source: str):
    result = db.execute(
        text("""
            SELECT last_value
            FROM etl_checkpoints
            WHERE source = :source
        """),
        {"source": source}
    ).fetchone()

    return result[0] if result else None


def update_checkpoint(db, source: str, last_value: str):
    db.execute(
        text("""
            INSERT INTO etl_checkpoints (source, last_value, updated_at)
            VALUES (:source, :last_value, NOW())
            ON CONFLICT (source)
            DO UPDATE SET
                last_value = :last_value,
                updated_at = NOW()
        """),
        {
            "source": source,
            "last_value": last_value
        }
    )
