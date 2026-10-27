import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"

def test_predict_endpoint():
    payload = {
        "timestamp": "2022-09-21 12:30:00",
        "from_bank": 20,
        "account": "100234",
        "to_bank": 3196,
        "receiver_account": "884129",
        "amount_received": 50000.0,
        "receiving_currency": "US Dollar",
        "amount_paid": 50000.0,
        "payment_currency": "US Dollar",
        "payment_format": "Wire"
    }
    res = client.post("/api/predict", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "probability" in data
    assert "prediction" in data
    assert "risk_level" in data

def test_transactions_endpoint():
    res = client.get("/api/transactions?limit=5")
    assert res.status_code == 200
    data = res.json()
    assert "items" in data
    assert "total" in data

def test_dashboard_stats_endpoint():
    res = client.get("/api/dashboard/stats")
    assert res.status_code == 200
    data = res.json()
    assert "kpis" in data

def test_model_info_endpoint():
    res = client.get("/api/model/info")
    assert res.status_code == 200
    data = res.json()
    assert data["model_name"] == "LightGBM"
