from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.db import get_db
from schemas.models import NormalizedCoin
from schemas.data_response import DataResponse
import time
import uuid

router = APIRouter()

@router.get("/data", response_model=DataResponse)
def get_data(
    page: int = 1,
    limit: int = 10,
    source: str | None = None,
    db: Session = Depends(get_db)
):
    start_time = time.time()
    request_id = str(uuid.uuid4())

    query = db.query(NormalizedCoin)

    if source:
        query = query.filter(NormalizedCoin.source == source)

    total = query.count()
    data = query.offset((page - 1) * limit).limit(limit).all()

    latency = round((time.time() - start_time) * 1000, 2)

    return {
        "metadata": {
            "request_id": request_id,
            "api_latency_ms": latency,
            "page": page,
            "limit": limit,
            "total_records": total
        },
        "data": [
            {
                "id": c.id,
                "source": c.source,
                "coin_id": c.coin_id,
                "name": c.name,
                "symbol": c.symbol,
                "market_cap": c.market_cap
            }
            for c in data
        ]
    }
