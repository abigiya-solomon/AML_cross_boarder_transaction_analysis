from fastapi import APIRouter
from app.ml.model_loader import model_loader

router = APIRouter()

@router.get("/health")
def health_check():
    if not model_loader.is_loaded:
        try:
            model_loader.load_artifacts()
        except Exception:
            pass

    return {
        "status": "healthy" if model_loader.is_loaded else "unhealthy",
        "model_loaded": model_loader.is_loaded,
        "model": model_loader.config.get("model_name", "LightGBM") if model_loader.config else "LightGBM"
    }
