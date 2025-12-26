from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    json_resp = response.json()
    assert "database" in json_resp
    assert json_resp["status"] == "ok"

def test_data_endpoint():
    response = client.get("/data")
    assert response.status_code == 200
    assert "data" in response.json()
    assert "metadata" in response.json()

def test_stats_endpoint():
    response = client.get("/stats")
    assert response.status_code == 200
    assert "total_runs" in response.json()
