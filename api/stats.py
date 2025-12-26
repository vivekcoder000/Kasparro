from fastapi import APIRouter, Depends
from core.db import get_db
from sqlalchemy.orm import Session
from services.stats_service import get_etl_stats

router = APIRouter()

@router.get("/stats")
def stats(db: Session = Depends(get_db)):
    return get_etl_stats(db)
