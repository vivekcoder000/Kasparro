from ingestion.api_coinpaprika import fetch_coinpaprika
from ingestion.csv_loader import load_csv_data
from services.etl_runner import normalize_data
from ingestion.api_coingecko import fetch_coingecko
from services.run_service import start_etl_run, mark_run_success, mark_run_failure

def run_etl():
    run_id = start_etl_run()
    print(f"Starting ETL Run ID: {run_id}")
    try:
        # Ingestion
        fetch_coinpaprika()
        fetch_coingecko()
        load_csv_data()
        
        # Normalization
        normalize_data()
        
        mark_run_success(run_id)
        print(f"ETL Run {run_id} Success")
        
    except Exception as e:
        mark_run_failure(run_id, str(e))
        print(f"ETL Run {run_id} Failed: {e}")
        raise

if __name__ == "__main__":
    run_etl()

