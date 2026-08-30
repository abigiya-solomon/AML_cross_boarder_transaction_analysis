import io
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.prediction import SinglePredictionRequest, PredictionResponse, BatchUploadResponse
from app.services.prediction_service import process_single_prediction, process_batch_upload

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def predict_single(
    payload: SinglePredictionRequest,
    db: Session = Depends(get_db)
):
    try:
        raw_dict = payload.model_dump()
        result = process_single_prediction(db, raw_dict)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )

@router.post("/predict/upload", response_model=BatchUploadResponse)
async def predict_upload(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV files are supported."
        )

    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))

        required_cols = [
            "From Bank", "Account", "To Bank", "Account.1",
            "Amount Received", "Receiving Currency", "Amount Paid",
            "Payment Currency", "Payment Format"
        ]
        
        # Flexibly check column aliases (lowercase vs standard header)
        col_map = {
            "from_bank": "From Bank",
            "account": "Account",
            "to_bank": "To Bank",
            "receiver_account": "Account.1",
            "amount_received": "Amount Received",
            "receiving_currency": "Receiving Currency",
            "amount_paid": "Amount Paid",
            "payment_currency": "Payment Currency",
            "payment_format": "Payment Format"
        }
        df = df.rename(columns=col_map)

        for col in required_cols:
            if col not in df.columns:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"CSV is missing required column: {col}"
                )

        summary = process_batch_upload(db, file.filename, df)
        return summary
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process CSV file: {str(e)}"
        )
