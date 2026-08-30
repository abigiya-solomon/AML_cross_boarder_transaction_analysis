from fastapi import APIRouter
from app.ml.model_loader import model_loader

router = APIRouter()

@router.get("/model/info")
def get_model_info():
    if not model_loader.is_loaded:
        try:
            model_loader.load_artifacts()
        except Exception:
            pass

    return {
        "model_name": "LightGBM",
        "threshold": 0.50,
        "feature_count": len(model_loader.feature_names) if model_loader.feature_names else 80,
        "evaluation_metrics": {
            "precision": 0.9167,
            "recall": 0.9987,
            "f1_score": 0.9559,
            "roc_auc": 0.9659,
            "pr_auc": 0.9673,
            "threshold": 0.50
        },
        "confusion_matrix": {
            "true_negatives": 473,
            "false_positives": 71,
            "false_negatives": 1,
            "true_positives": 781,
            "total_test_samples": 1326
        },
        "compared_models": [
            "Logistic Regression",
            "Random Forest",
            "Extra Trees",
            "HistGradientBoosting",
            "XGBoost",
            "LightGBM",
            "CatBoost"
        ],
        "feature_categories": {
            "sender_behavioral_features": 10,
            "receiver_behavioral_features": 10,
            "relationship_features": 4,
            "bank_knowledge_features": 2,
            "transaction_and_temporal_features": 17,
            "total_raw_engineered_features": 43,
            "processed_one_hot_features": 80
        }
    }
