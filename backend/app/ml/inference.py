import pandas as pd
import numpy as np
from app.ml.model_loader import model_loader
from app.ml.feature_engineering import build_feature_dataframe
from app.config import settings

def determine_risk_level(probability: float) -> str:
    """Categorizes probability into AML risk tiers."""
    if probability >= 0.85:
        return "CRITICAL"
    elif probability >= 0.70:
        return "HIGH"
    elif probability >= 0.50:
        return "MEDIUM"
    else:
        return "LOW"

def predict_transaction(transaction_dict: dict, history_stats: dict = None) -> dict:
    """End-to-end inference for a single raw transaction."""
    if not model_loader.is_loaded:
        model_loader.load()

    # 1. Feature Engineering: outputs 43 features
    features_df = build_feature_dataframe(transaction_dict, history_stats)

    # 2. Preprocessor transformation: produces 80 one-hot features
    processed_matrix = model_loader.preprocessor.transform(features_df)
    
    # Handle sparse matrix if output is sparse
    if hasattr(processed_matrix, "toarray"):
        processed_matrix = processed_matrix.toarray()

    # 3. Wrap in DataFrame with exact processed feature names to preserve feature names for LightGBM
    processed_df = pd.DataFrame(processed_matrix, columns=model_loader.feature_names)

    # 4. LightGBM predict_proba
    probabilities = model_loader.model.predict_proba(processed_df)
    prob_suspicious = float(probabilities[0, 1])

    # 5. Threshold (0.50)
    threshold = settings.CLASSIFICATION_THRESHOLD
    prediction = int(prob_suspicious >= threshold)
    label = "Suspicious" if prediction == 1 else "Normal"
    risk_level = determine_risk_level(prob_suspicious)

    return {
        "probability": round(prob_suspicious, 4),
        "prediction": prediction,
        "threshold": threshold,
        "label": label,
        "risk_level": risk_level,
        "model_name": model_loader.model_config.get("model_name", "LightGBM"),
        "model_version": "1.0.0",
        "engineered_features": features_df.iloc[0].to_dict(),
    }
