from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.transaction_service import get_transactions_list, get_transaction_detail

router = APIRouter()

@router.get("/transactions")
def list_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    suspicious_only: bool = Query(False),
    risk_level: str = Query(None),
    currency: str = Query(None),
    payment_format: str = Query(None),
    search: str = Query(None),
    sort_by: str = Query("timestamp"),
    sort_order: str = Query("desc"),
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
def transaction_detail(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    detail = get_transaction_detail(db, transaction_id)
    if not detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with ID {transaction_id} not found."
        )
    return detail
