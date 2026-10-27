from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, or_
from app.db.models import TransactionModel, PredictionModel
from app.schemas.prediction import PaginatedTransactionsResponse, TransactionWithPredictionResponse

def get_transactions_list(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    suspicious_only: bool = False,
    risk_level: Optional[str] = None,
    currency: Optional[str] = None,
    payment_format: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = "timestamp",
    sort_order: str = "desc"
) -> PaginatedTransactionsResponse:
    query = db.query(TransactionModel, PredictionModel).join(
        PredictionModel, TransactionModel.id == PredictionModel.transaction_id
    )

    if suspicious_only:
        query = query.filter(PredictionModel.prediction == 1)

    if risk_level and risk_level.upper() != "ALL":
        query = query.filter(PredictionModel.risk_level == risk_level.upper())

    if currency and currency.upper() != "ALL":
        query = query.filter(
            or_(
                TransactionModel.receiving_currency == currency,
                TransactionModel.payment_currency == currency
            )
        )

    if payment_format and payment_format.upper() != "ALL":
        query = query.filter(TransactionModel.payment_format == payment_format)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                TransactionModel.account.like(search_term),
                TransactionModel.receiver_account.like(search_term),
                TransactionModel.from_bank.like(search_term),
                TransactionModel.to_bank.like(search_term)
            )
        )

    # Sorting
    sort_col = getattr(TransactionModel, sort_by, None)
    if not sort_col:
        sort_col = getattr(PredictionModel, sort_by, TransactionModel.timestamp)

    if sort_order.lower() == "asc":
        query = query.order_by(asc(sort_col))
    else:
        query = query.order_by(desc(sort_col))

    total = query.count()
    results = query.offset(skip).limit(limit).all()

    items = []
    for tx, pred in results:
        items.append(
            TransactionWithPredictionResponse(
                id=tx.id,
                timestamp=tx.timestamp.strftime("%Y-%m-%d %H:%M:%S") if tx.timestamp else None,
                from_bank=tx.from_bank,
                account=tx.account,
                to_bank=tx.to_bank,
                receiver_account=tx.receiver_account,
                amount_received=tx.amount_received,
                receiving_currency=tx.receiving_currency,
                amount_paid=tx.amount_paid,
                payment_currency=tx.payment_currency,
                payment_format=tx.payment_format,
                created_at=tx.created_at,
                probability=pred.probability,
                prediction=pred.prediction,
                label=pred.label,
                risk_level=pred.risk_level,
            )
        )

    return PaginatedTransactionsResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=items
    )
