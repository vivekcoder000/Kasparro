from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, JSON, DateTime, UniqueConstraint
from datetime import datetime
from sqlalchemy import Boolean

Base = declarative_base()

class RawCoinPaprika(Base):
    __tablename__ = "raw_coinpaprika"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    data = Column(JSON)
    fetched_at = Column(DateTime, default=datetime.utcnow)

class RawCSV(Base):
    __tablename__ = "raw_csv"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    data = Column(JSON)
    fetched_at = Column(DateTime, default=datetime.utcnow)

class NormalizedCoin(Base):
    __tablename__ = "normalized_coins"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    source = Column(String)            # coinpaprika / csv / coingecko later
    coin_id = Column(String)
    name = Column(String)
    symbol = Column(String)
    market_cap = Column(String)

    __table_args__ = (
        UniqueConstraint("source", "coin_id", name="unique_coin_per_source"),
    )

class RawCoinGecko(Base):
    __tablename__ = "raw_coingecko"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON)
    fetched_at = Column(DateTime, default=datetime.utcnow)

class ETLRun(Base):
    __tablename__ = "etl_runs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    started_at = Column(DateTime)
    finished_at = Column(DateTime)
    status = Column(String)     # success or failed
    records_processed = Column(Integer)

class ETLCheckpoint(Base):
    __tablename__ = "etl_checkpoints"

    source = Column(String, primary_key=True)
    last_value = Column(String)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)



