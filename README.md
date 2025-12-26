# Kasparro Backend ETL

## Overview
A robust, restart-safe ETL backend for crypto data. It ingests data from multiple sources (simulated APIs, CSVs), normalizes it into a unified schema, and exposes it via a fast REST API.

## Features
- **Incremental ETL**: Uses checkpoints to avoid re-processing old data.
- **Restart Safety**: Tracks run status (`running`/`success`/`failed`) to handle crashes gracefully.
- **Hybrid Architecture**: Designed to run the FastAPI app natively on Windows while keeping the Database in Docker for stability.
- **Observability**: Dedicated `/health` and `/stats` endpoints.

## Quick Start

### Prerequisites
- Docker Desktop
- Python 3.11+
- Git Bash or PowerShell

### Running the System
1. **Start Database**:
   ```bash
   docker-compose up -d db
   ```
2. **Install Dependencies**:
   ```bash
   .\venv\Scripts\pip install -r requirements.txt
   ```
3. **Initialize Database**:
   ```bash
   .\venv\Scripts\python create_tables.py
   ```
4. **Run Server**:
   ```bash
   .\venv\Scripts\python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   *Access API docs at [http://localhost:8000/docs](http://localhost:8000/docs)*

5. **Run ETL Manually**:
   ```bash
   .\venv\Scripts\python run_etl.py
   ```

### Testing
Run the full test suite (requires DB to be running):
```bash
.\venv\Scripts\python -m pytest
```

## Architecture

### Data Flow
1. **Ingestion**: `ingestion/` scripts fetch data from CoinPaprika, CoinGecko, and CSVs.
2. **Filtering**: Checkpoints (`etl_checkpoints` table) are queried to skip already processed records (Idempotency).
3. **Normalization**: Raw data is transformed and strictly typed before insertion into `normalized_coins`.
4. **Serving**: FastAPI serves data via `/data` with pagination and filtering.

### Key Components
- **`services/checkpoint_service.py`**: Manages granular extraction cursors.
- **`services/etl_runner.py`**: Orchestrates the normalization process.
- **`api/stats.py`**: Provides pipeline metrics (`last_success`, `total_runs`).

## Design Decisions
- **Raw Tables**: We store raw JSON first (`raw_coinpaprika`, etc.) to allow re-processing if business logic changes.
- **Checkpoints**: Essential for performance; prevents ingesting millions of duplicate rows on restart.
- **Hybrid Mode**: Solves Windows/Docker networking issues by keeping the API on the host network.
