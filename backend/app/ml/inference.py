import pandas as pd
import numpy as np

from app.ml.model_loader import model_loader
from app.ml.feature_engineering import build_raw_feature_df, MODEL_NUMERIC_FEATURES, MODEL_CATEGORICAL_FEATURES
from app.config import settings

def get_risk_level(probability: float) -> str:
    if probability < 0.30:
        return "LOW"
    elif probability < 0.70:
        return "MEDIUM"
    elif probability < 0.90:
        return "HIGH"
    else:
        return "CRITICAL"

def predict_single_transaction(raw_tx_dict: dict, account_stats: dict = None) -> dict:
    if not model_loader.is_loaded:
        model_loader.load_artifacts()

    feature_df = build_raw_feature_df(raw_tx_dict, account_stats)

    expected_cols = MODEL_NUMERIC_FEATURES + MODEL_CATEGORICAL_FEATURES
    if list(feature_df.columns) != expected_cols:
        raise ValueError(
            f"Feature mismatch! Expected {len(expected_cols)} columns, got {len(feature_df.columns)}."
        )

    processed_matrix = model_loader.preprocessor.transform(feature_df)

    processed_df = pd.DataFrame(
        processed_matrix,
        columns=model_loader.feature_names,
        index=feature_df.index
    )

    if len(processed_df.columns) != len(model_loader.feature_names):
        raise ValueError(
            f"Processed feature count ({len(processed_df.columns)}) does not match model expected features ({len(model_loader.feature_names)})."
        )

    probabilities = model_loader.model.predict_proba(processed_df)[:, 1]
    probability = float(probabilities[0])

    threshold = settings.PREDICTION_THRESHOLD
    prediction = int(probability >= threshold)
    label = "Suspicious" if prediction == 1 else "Normal"
    risk_level = get_risk_level(probability)

    engineered_features = feature_df.to_dict(orient="records")[0]

    return {
        "prediction": prediction,
        "label": label,
        "probability": round(probability, 4),
        "threshold": threshold,
        "risk_level": risk_level,
        "model_name": model_loader.config.get("model_name", "LightGBM"),
        "model_version": "1.0",
        "engineered_features": engineered_features,
    }

def predict_batch_df(df: pd.DataFrame) -> list:
    if not model_loader.is_loaded:
        model_loader.load_artifacts()

    results = []
    for idx, row in df.iterrows():
        tx_dict = {
            "Timestamp": str(row.get("Timestamp", "2022-09-21 12:30:00")),
            "From Bank": int(row.get("From Bank", row.get("from_bank", 100))),
            "Account": str(row.get("Account", row.get("account", "111111"))),
            "To Bank": int(row.get("To Bank", row.get("to_bank", 200))),
            "Account.1": str(row.get("Account.1", row.get("receiver_account", "222222"))),
            "Amount Received": float(row.get("Amount Received", row.get("amount_received", 1000.0))),
            "Receiving Currency": str(row.get("Receiving Currency", row.get("receiving_currency", "US Dollar"))),
            "Amount Paid": float(row.get("Amount Paid", row.get("amount_paid", 1000.0))),
            "Payment Currency": str(row.get("Payment Currency", row.get("payment_currency", "US Dollar"))),
            "Payment Format": str(row.get("Payment Format", row.get("payment_format", "Wire"))),
        }
        res = predict_single_transaction(tx_dict)
        results.append((tx_dict, res))

    return results
