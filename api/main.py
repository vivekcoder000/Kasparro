from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler

from api.health import router as health_router
from api.data import router as data_router
from api.stats import router as stats_router

from ingestion.api_coinpaprika import fetch_coinpaprika
from ingestion.api_coingecko import fetch_coingecko
from ingestion.csv_loader import load_csv_data
from services.etl_runner import normalize_data

def run_scheduled_etl():
    print("🔥 Scheduled ETL Started")
    try:
        fetch_coinpaprika()
        fetch_coingecko()
        load_csv_data()
        normalize_data()
        print("✅ Scheduled ETL Completed")
    except Exception as e:
        print("❌ Scheduled ETL Failed:", e)

app = FastAPI(
    title="Kasparro Backend API",
    description="ETL-backed Crypto Data API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(data_router)
app.include_router(stats_router)

@app.get("/")
def root():
    return {
        "message": "Kasparro Backend API is running 🚀",
        "endpoints": {
            "health": "/health",
            "data": "/data",
            "stats": "/stats",
            "docs": "/docs"
        }
    }

scheduler = BackgroundScheduler()
scheduler.add_job(run_scheduled_etl, "interval", hours=1)
scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()
