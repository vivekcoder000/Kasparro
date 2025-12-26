import requests
from core.db import SessionLocal
from schemas.models import RawCoinGecko

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/list"

from services.checkpoint_service import get_checkpoint, update_checkpoint

def fetch_coingecko(db=None):
    print("Fetching data from CoinGecko...")
    should_close_db = False
    if db is None:
        db = SessionLocal()
        should_close_db = True

    try:
        try:
            response = requests.get(COINGECKO_URL, timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print("⚠️ Could not fetch CoinGecko data")
            print(e)
            return

        last_val = get_checkpoint(db, "coingecko")
        last_idx = int(last_val) if last_val else -1

        new_items = []
        max_idx = last_idx

        for i, item in enumerate(data):
            if i <= last_idx:
                continue
            new_items.append(item)
            max_idx = i

        if new_items:
            record = RawCoinGecko(data=new_items)
            db.add(record)
            update_checkpoint(db, "coingecko", str(max_idx))
            db.commit()
            print(f"CoinGecko: Saved {len(new_items)} new records.")
        else:
            print("CoinGecko: No new records found.")

    except Exception as e:
        db.rollback()
        print("CoinGecko save failed")
        print(e)
    finally:
        if should_close_db:
            db.close()
