from sqlalchemy import text

def test_etl_is_idempotent(db_session):
    from run_etl import run_etl

    # Run ETL first time
    run_etl()

    # Count records after first run
    first_count = db_session.execute(
        text("SELECT COUNT(*) FROM normalized_coins")
    ).scalar()

    # Run ETL second time
    run_etl()

    # Count records again
    second_count = db_session.execute(
        text("SELECT COUNT(*) FROM normalized_coins")
    ).scalar()

    # Should NOT increase
    assert first_count == second_count
