# Kasparro Backend & ETL System 🚀

A production-grade backend system built as part of Kasparro assignment.  
This system ingests cryptocurrency data, cleans and normalizes it, stores it in PostgreSQL, exposes APIs, and runs scheduled ETL — all deployed in the cloud.

---

## 🌍 Live Deployment

API Base URL:
https://kasparro-backend-naveen-kumar-production.up.railway.app/

Useful Endpoints:
- `/` → Welcome
- `/health` → System + DB health
- `/data` → Paginated normalized crypto data
- `/stats` → ETL run analytics
- `/docs` → Swagger UI

---

## 🧠 System Architecture
**Built with**
- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Docker
- Railway Cloud
- APScheduler (cloud scheduling)
- PyTest (automated tests)

**Flow**
1️⃣ Fetch from CoinPaprika  
2️⃣ Fetch from CoinGecko  
3️⃣ Load CSV  
4️⃣ Store Raw  
5️⃣ Normalize  
6️⃣ Store final structured dataset  
7️⃣ Serve via API  
8️⃣ Repeat automatically on schedule

---

## 🗄️ Database Design
Tables:
- `RawCoinPaprika`
- `RawCSV`
- `NormalizedCoin`
- `ETLRun / ETLCheckpoint`

Supports:
- Incremental ETL
- Resume safe behavior
- Monitoring

---

## 🐳 Docker Support

docker-compose up --build

Services:
- FastAPI backend
- PostgreSQL DB
- Automatic ETL on startup

---

## ⏰ Scheduling
Cloud scheduler automatically runs ETL every **1 hour** using APScheduler.

Fully automated.
No manual trigger required.
Logs available in Railway dashboard.

---

## 🧪 Automated Tests

pytest -v

Covers:
✔ `/health` endpoint  
✔ `/data` endpoint  
✔ ETL functionality  
✔ Failure simulation (database break test)

Ensures production reliability and developer confidence.

---

## 🚀 Deployment
Deployed on Railway:
- Backend Service
- PostgreSQL DB
- Docker
- Environment Variables configured
- Auto redeploy from GitHub
- Persistent logs

---

## 🏁 Features Completed for Assignment

✔ Dockerized Backend  
✔ Clean Architecture  
✔ PostgreSQL Integration  
✔ Cloud Deployment  
✔ ETL Pipelines  
✔ Incremental Processing  
✔ Recovery Logic  
✔ Public APIs  
✔ Scheduling  
✔ Automated Testing  
✔ Monitoring & Logs  
✔ Professional Documentation  

---

## 👨‍💻 Developer
Name: Naveen Kumar  
Email: naveeengulgi2003@gmail.com
