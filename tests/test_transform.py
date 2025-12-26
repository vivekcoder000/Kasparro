from pydantic import BaseModel

class NormalizedRecord(BaseModel):
    source: str
    external_id: str
    name: str
    symbol: str
    market_cap: float = None

def normalize_api(raw):
    return NormalizedRecord(
        source="api",
        external_id=str(raw["id"]),
        name=raw["name"],
        symbol=raw["symbol"],
        market_cap=raw.get("market_cap")
    )

def test_api_record_normalization():
    raw_record = {
        "id": 123,
        "name": "Bitcoin",
        "symbol": "BTC",
        "market_cap": 1000,
        "created_at": "2024-01-01T00:00:00"
    }

    record = normalize_api(raw_record)

    assert record.source == "api"
    assert record.external_id == "123"
    assert record.name == "Bitcoin"
