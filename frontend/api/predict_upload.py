# predict_upload.py
from fastapi import FastAPI, File, UploadFile, HTTPException
import io
import pandas as pd
from app.ml.model_loader import model_loader
from app.services.prediction_service import process_batch_upload  # or call local inference per-row

app = FastAPI()

@app.post("/")
async def upload(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV supported")
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))
    if not model_loader.is_loaded:
        model_loader.load_artifacts()
    # process_batch_upload can be adapted to run without DB or to return summary only
    summary = process_batch_upload(None, file.filename, df)  # adapt as needed
    return summary