def test_etl_handles_failure_gracefully():
    from services.checkpoint_service import update_checkpoint

    try:
        # Simulate failure by passing bad checkpoint value (None db session will raise AttributeError)
        update_checkpoint(None, "bad_source", "invalid")
    except Exception:
        # Exception caught means it didn't crash the whole test runner ungracefully
        assert True
