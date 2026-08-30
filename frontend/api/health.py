# health.py
from fastapi import FastAPI
from app.ml.model_loader import model_loader

app = FastAPI()

@app.get("/")
def health():
    if not model_loader.is_loaded:
        try:
            model_loader.load_artifacts()
        except Exception:
            pass
    return {
        "status": "healthy" if model_loader.is_loaded else "unhealthy",
        "model_loaded": model_loader.is_loaded,
    }