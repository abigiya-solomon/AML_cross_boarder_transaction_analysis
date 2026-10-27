from fastapi import APIRouter
from app.ml.model_loader import model_loader
from app.config import settings

router = APIRouter(tags=["Model Performance"])

@router.get("/model/info")
def get_model_info():
    return {
        "model_name": "LightGBM",
        "model_type": "LGBMClassifier",
        "version": "1.0.0",
        "evaluation_metrics": {
            "precision": 0.9167,
            "recall": 0.9987,
            "f1_score": 0.9559,
            "roc_auc": 0.9659,
            "pr_auc": 0.9673,
            "threshold": 0.50,
        },
        "confusion_matrix": {
            "true_negatives": 473,
            "false_positives": 71,
            "false_negatives": 1,
            "true_positives": 781,
            "total_test_samples": 1326,
        },
        "features": {
            "total_features": len(model_loader.feature_names) if model_loader.feature_names is not None else 80,
            "threshold": settings.CLASSIFICATION_THRESHOLD,
        },
        "comparison_candidates": [
            {"model": "Logistic Regression", "f1": 0.8912, "pr_auc": 0.9124},
            {"model": "Random Forest", "f1": 0.9341, "pr_auc": 0.9412},
            {"model": "Extra Trees", "f1": 0.9388, "pr_auc": 0.9475},
            {"model": "HistGradientBoosting", "f1": 0.9452, "pr_auc": 0.9582},
            {"model": "XGBoost", "f1": 0.9470, "pr_auc": 0.9591},
            {"model": "LightGBM", "f1": 0.9559, "pr_auc": 0.9673, "selected": True},
            {"model": "CatBoost", "f1": 0.9463, "pr_auc": 0.9579},
        ]
    }
