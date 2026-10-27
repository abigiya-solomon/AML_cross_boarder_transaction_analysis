from fastapi import APIRouter
from app.ml.model_loader import model_loader
from app.config import settings

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "model_loaded": model_loader.is_loaded,
        "model_name": model_loader.model_config.get("model_name", "LightGBM") if model_loader.is_loaded else None,
        "threshold": settings.CLASSIFICATION_THRESHOLD,
    }
