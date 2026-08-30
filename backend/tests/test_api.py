import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True
    assert data["model"] == "LightGBM"

def test_predict_endpoint():
    payload = {
        "timestamp": "2022-09-21 12:30:00",
        "from_bank": 123,
        "account": "456789",
        "to_bank": 987,
        "receiver_account": "123456",
        "amount_received": 10000.0,
        "receiving_currency": "US Dollar",
        "amount_paid": 10000.0,
        "payment_currency": "US Dollar",
        "payment_format": "Wire"
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "probability" in data
    assert data["threshold"] == 0.50
    assert "risk_level" in data

def test_transactions_endpoint():
    response = client.get("/api/transactions")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data

def test_dashboard_stats_endpoint():
    response = client.get("/api/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert "kpis" in data
    assert "suspicious_over_time" in data
    assert "risk_distribution" in data

def test_model_info_endpoint():
    response = client.get("/api/model/info")
    assert response.status_code == 200
    data = response.json()
    assert data["model_name"] == "LightGBM"
    assert data["threshold"] == 0.50
    assert data["evaluation_metrics"]["precision"] == 0.9167
    assert data["evaluation_metrics"]["recall"] == 0.9987
