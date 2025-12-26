import csv
from core.db import SessionLocal
from schemas.models import RawCSV

from services.checkpoint_service import get_checkpoint, update_checkpoint

def load_csv_data(db=None):
    print("Reading CSV...")
    should_close_db = False
    if db is None:
        db = SessionLocal()
        should_close_db = True

    try:
        with open("data/crypto_sample.csv", mode="r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

            last_val = get_checkpoint(db, "csv")
            last_idx = int(last_val) if last_val else -1

            new_rows = []
            max_idx = last_idx

            for i, row in enumerate(rows):
                if i <= last_idx:
                    continue
                new_rows.append(row)
                max_idx = i

            if new_rows:
                record = RawCSV(data=new_rows)
                db.add(record)
                update_checkpoint(db, "csv", str(max_idx))
                db.commit()
                print(f"CSV: Stored {len(new_rows)} new rows.")
            else:
                print("CSV: No new rows found.")

    except Exception as e:
        db.rollback()
        print("CSV ingestion failed")
        print(e)

    finally:
        if should_close_db:
            db.close()
