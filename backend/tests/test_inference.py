import pytest
from app.ml.feature_engineering import build_feature_dataframe, MODEL_NUMERIC_FEATURES, MODEL_CATEGORICAL_FEATURES
from app.ml.model_loader import model_loader
from app.ml.inference import predict_transaction

sample_tx = {
    "timestamp": "2022-09-21 12:30:00",
    "from_bank": 20,
    "account": "100234",
    "to_bank": 3196,
    "receiver_account": "884129",
    "amount_received": 15000.0,
    "receiving_currency": "US Dollar",
    "amount_paid": 15000.0,
    "payment_currency": "US Dollar",
    "payment_format": "Wire"
}

def test_feature_engineering_shape():
    df = build_feature_dataframe(sample_tx)
    assert df.shape[1] == len(MODEL_NUMERIC_FEATURES) + len(MODEL_CATEGORICAL_FEATURES)
    assert "Unknown_Unknown_Transfer" in df.columns
    assert "Sender_Transaction_Count" in df.columns

def test_single_prediction():
    res = predict_transaction(sample_tx)
    assert "probability" in res
    assert 0.0 <= res["probability"] <= 1.0
    assert res["prediction"] in (0, 1)
    assert res["threshold"] == 0.50
    assert res["risk_level"] in ("LOW", "MEDIUM", "HIGH", "CRITICAL")
