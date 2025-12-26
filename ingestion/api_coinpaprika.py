import requests
from core.db import SessionLocal
from schemas.models import RawCoinPaprika

COINPAPRIKA_URL = "https://api.coinpaprika.com/v1/coins"

from services.checkpoint_service import get_checkpoint, update_checkpoint

def fetch_coinpaprika(db=None):
    print("Fetching data from CoinPaprika...")
    should_close_db = False
    if db is None:
        db = SessionLocal()
        should_close_db = True

    try:
        response = requests.get(COINPAPRIKA_URL)
        response.raise_for_status()
        data = response.json()

        last_val = get_checkpoint(db, "coinpaprika")
        last_idx = int(last_val) if last_val else -1

        new_items = []
        max_idx = last_idx

        for i, item in enumerate(data):
            if i <= last_idx:
                continue
            new_items.append(item)
            max_idx = i

        if new_items:
            record = RawCoinPaprika(data=new_items)
            db.add(record)
            update_checkpoint(db, "coinpaprika", str(max_idx))
            db.commit()
            print(f"CoinPaprika: Saved {len(new_items)} new records.")
        else:
            print("CoinPaprika: No new records found (Checkpoint up to date).")

    except Exception as e:
        db.rollback()
        print("Failed to save CoinPaprika data")
        print(e)
    finally:
        if should_close_db:
            db.close()
