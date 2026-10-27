import json
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import TransactionModel, PredictionModel
from app.schemas.prediction import PaginatedTransactionsResponse
from app.services.transaction_service import get_transactions_list

router = APIRouter(tags=["Transactions"])

@router.get("/transactions", response_model=PaginatedTransactionsResponse)
def list_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    suspicious_only: bool = False,
    risk_level: Optional[str] = "ALL",
    currency: Optional[str] = "ALL",
    payment_format: Optional[str] = "ALL",
    search: Optional[str] = None,
    sort_by: str = "timestamp",
    sort_order: str = "desc",
    db: Session = Depends(get_db)
):
    return get_transactions_list(
        db=db,
        skip=skip,
        limit=limit,
        suspicious_only=suspicious_only,
        risk_level=risk_level,
        currency=currency,
        payment_format=payment_format,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order
    )

@router.get("/transactions/{transaction_id}")
def get_transaction_detail(transaction_id: int, db: Session = Depends(get_db)):
    tx = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found.")

    pred = db.query(PredictionModel).filter(PredictionModel.transaction_id == transaction_id).first()
    engineered_dict = json.loads(pred.engineered_features) if (pred and pred.engineered_features) else None

    return {
        "transaction": {
            "id": tx.id,
            "timestamp": tx.timestamp.strftime("%Y-%m-%d %H:%M:%S") if tx.timestamp else None,
            "from_bank": tx.from_bank,
            "account": tx.account,
            "to_bank": tx.to_bank,
            "receiver_account": tx.receiver_account,
            "amount_received": tx.amount_received,
            "receiving_currency": tx.receiving_currency,
            "amount_paid": tx.amount_paid,
            "payment_currency": tx.payment_currency,
            "payment_format": tx.payment_format,
            "created_at": tx.created_at,
        },
        "model_result": {
            "probability": pred.probability if pred else None,
            "prediction": pred.prediction if pred else None,
            "label": pred.label if pred else None,
            "risk_level": pred.risk_level if pred else None,
            "threshold": pred.threshold if pred else 0.50,
            "model_name": pred.model_name if pred else "LightGBM",
            "model_version": pred.model_version if pred else "1.0.0",
        },
        "engineered_features": engineered_dict,
    }
