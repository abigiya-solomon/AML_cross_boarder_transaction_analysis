from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.prediction import SinglePredictionRequest, PredictionResponse, BatchUploadResponse
from app.services.prediction_service import create_single_prediction, process_batch_csv

router = APIRouter(tags=["Predictions"])

@router.post("/predict", response_model=PredictionResponse)
def predict_single(request: SinglePredictionRequest, db: Session = Depends(get_db)):
    try:
        result = create_single_prediction(request.model_dump(), db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@router.post("/predict/upload", response_model=BatchUploadResponse)
async def predict_batch(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")
    try:
        contents = await file.read()
        summary = process_batch_csv(contents, file.filename, db)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process CSV upload: {str(e)}")
