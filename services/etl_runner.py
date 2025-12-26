from schemas.models import RawCoinGecko, RawCoinPaprika, RawCSV, NormalizedCoin, ETLRun
from datetime import datetime
from core.db import SessionLocal
from services.checkpoint_service import get_checkpoint, update_checkpoint

def normalize_data():
    db = SessionLocal()
    start_time = datetime.utcnow()
    total_records = 0
    
    print("Normalizing data incrementally...")

    try:
        # Get last normalized timestamp from checkpoint
        last_val = get_checkpoint(db, "normalization_timestamp")
        last_time = datetime.fromisoformat(last_val) if last_val else None
        
        if last_time:
            print(f"Resuming normalization from: {last_time}")

        # Helper function to safe insert (Idempotency)
        def safe_add_coin(coin_data):
            exists = db.query(NormalizedCoin).filter_by(
                source=coin_data["source"],
                coin_id=coin_data["coin_id"]
            ).first()
            
            if not exists:
                db.add(NormalizedCoin(**coin_data))
                return True
            return False

        # CoinPaprika
        paprika_records = db.query(RawCoinPaprika).all()
        for record in paprika_records:
            if not last_time or record.fetched_at > last_time:
                for coin in record.data:
                    added = safe_add_coin({
                        "source": "coinpaprika",
                        "coin_id": coin.get("id"),
                        "name": coin.get("name"),
                        "symbol": coin.get("symbol"),
                        "market_cap": None
                    })
                    if added: total_records += 1

        # CSV
        csv_records = db.query(RawCSV).all()
        for record in csv_records:
            if not last_time or record.fetched_at > last_time:
                for row in record.data:
                    added = safe_add_coin({
                        "source": "csv",
                        "coin_id": row.get("id"),
                        "name": row.get("name"),
                        "symbol": row.get("symbol"),
                        "market_cap": row.get("market_cap")
                    })
                    if added: total_records += 1

        # CoinGecko
        gecko_records = db.query(RawCoinGecko).all()
        for record in gecko_records:
            if not last_time or record.fetched_at > last_time:
                for coin in record.data:
                    added = safe_add_coin({
                        "source": "coingecko",
                        "coin_id": coin.get("id"),
                        "name": coin.get("name"),
                        "symbol": coin.get("symbol"),
                        "market_cap": None
                    })
                    if added: total_records += 1

        # Update checkpoint
        update_checkpoint(db, "normalization_timestamp", start_time.isoformat())
        db.commit()

        print(f"Incremental normalization completed. Processed {total_records} records.")

    except Exception as e:
        db.rollback()
        print("Normalization failed")
        print(e)
        raise e

    finally:
        db.close()
