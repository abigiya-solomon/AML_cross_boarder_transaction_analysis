# predict.py
from fastapi import FastAPI, Request, HTTPException
from app.ml.model_loader import model_loader
from app.ml.inference import predict_single_transaction  # function that accepts raw dict

app = FastAPI()

@app.post("/")
async def predict(request: Request):
    payload = await request.json()
    if not model_loader.is_loaded:
        model_loader.load_artifacts()
    try:
        # adapt payload shape if needed; predict_single_transaction expects a raw dict
        result = predict_single_transaction(payload)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))