import pytest
from app.ml.model_loader import model_loader
from app.ml.feature_engineering import build_raw_feature_df, MODEL_NUMERIC_FEATURES, MODEL_CATEGORICAL_FEATURES
from app.ml.inference import predict_single_transaction, get_risk_level

def test_model_loader():
    model_loader.load_artifacts()
    assert model_loader.is_loaded is True
    assert model_loader.model is not None
    assert model_loader.preprocessor is not None
    assert len(model_loader.feature_names) == 80
    assert model_loader.config["threshold"] == 0.50

def test_feature_engineering_shape():
    raw_tx = {
        "Timestamp": "2022-09-21 12:30:00",
        "From Bank": 123,
        "Account": "456789",
        "To Bank": 987,
        "Account.1": "123456",
        "Amount Received": 10000.0,
        "Receiving Currency": "US Dollar",
        "Amount Paid": 10000.0,
        "Payment Currency": "US Dollar",
        "Payment Format": "Wire"
    }
    df = build_raw_feature_df(raw_tx)
    expected_raw_cols = MODEL_NUMERIC_FEATURES + MODEL_CATEGORICAL_FEATURES
    assert len(df.columns) == 43
    assert list(df.columns) == expected_raw_cols

def test_single_prediction():
    raw_tx = {
        "Timestamp": "2022-09-21 12:30:00",
        "From Bank": 123,
        "Account": "456789",
        "To Bank": 987,
        "Account.1": "123456",
        "Amount Received": 10000.0,
        "Receiving Currency": "US Dollar",
        "Amount Paid": 10000.0,
        "Payment Currency": "US Dollar",
        "Payment Format": "Wire"
    }
    res = predict_single_transaction(raw_tx)
    assert "probability" in res
    assert "prediction" in res
    assert res["prediction"] in [0, 1]
    assert res["threshold"] == 0.50
    assert res["risk_level"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    assert res["label"] in ["Normal", "Suspicious"]
