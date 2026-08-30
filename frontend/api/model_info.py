# model_info.py
from fastapi import FastAPI
from app.ml.model_loader import model_loader

app = FastAPI()

@app.get("/")
def model_info():
    if not model_loader.is_loaded:
        try:
            model_loader.load_artifacts()
        except Exception:
            pass
    return {
        "model_name": model_loader.config.get("model_name", "LightGBM") if model_loader.config else "LightGBM",
        "feature_count": len(model_loader.feature_names) if model_loader.feature_names else None
    }