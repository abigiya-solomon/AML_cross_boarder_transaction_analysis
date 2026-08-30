from sqlalchemy.orm import Session
from sqlalchemy import desc, or_, and_
from app.db.models import TransactionModel, PredictionModel
from app.ml.feature_engineering import build_raw_feature_df

def get_transactions_list(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    suspicious_only: bool = False,
    risk_level: str = None,
    currency: str = None,
    payment_format: str = None,
    search: str = None,
    sort_by: str = "timestamp",
    sort_order: str = "desc"
):
    query = db.query(TransactionModel, PredictionModel).join(
        PredictionModel, TransactionModel.id == PredictionModel.transaction_id
    )

    if suspicious_only:
        query = query.filter(PredictionModel.prediction == 1)

    if risk_level and risk_level.upper() != "ALL":
        query = query.filter(PredictionModel.risk_level == risk_level.upper())

    if currency and currency.lower() != "all":
        query = query.filter(
            or_(
                TransactionModel.receiving_currency == currency,
                TransactionModel.payment_currency == currency
            )
        )

    if payment_format and payment_format.lower() != "all":
        query = query.filter(TransactionModel.payment_format == payment_format)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                TransactionModel.account.like(search_term),
                TransactionModel.receiver_account.like(search_term),
                TransactionModel.from_bank.cast(String).like(search_term),
                TransactionModel.to_bank.cast(String).like(search_term),
            )
        )

    total_count = query.count()

    if sort_by == "probability":
        order_col = PredictionModel.probability
    elif sort_by == "amount":
        order_col = TransactionModel.amount_received
    else:
        order_col = TransactionModel.timestamp

    if sort_order == "desc":
        query = query.order_by(desc(order_col))
    else:
        query = query.order_by(order_col)

    results = query.offset(skip).limit(limit).all()

    items = []
    for tx, pred in results:
        items.append({
            "id": tx.id,
            "timestamp": str(tx.timestamp),
            "from_bank": tx.from_bank,
            "account": tx.account,
            "to_bank": tx.to_bank,
            "receiver_account": tx.receiver_account,
            "amount_received": tx.amount_received,
            "amount_paid": tx.amount_paid,
            "receiving_currency": tx.receiving_currency,
            "payment_currency": tx.payment_currency,
            "payment_format": tx.payment_format,
            "probability": pred.probability,
            "prediction": pred.prediction,
            "label": "Suspicious" if pred.prediction == 1 else "Normal",
            "risk_level": pred.risk_level,
            "threshold": pred.threshold,
        })

    return {
        "total": total_count,
        "skip": skip,
        "limit": limit,
        "items": items,
    }

def get_transaction_detail(db: Session, transaction_id: int):
    result = db.query(TransactionModel, PredictionModel).join(
        PredictionModel, TransactionModel.id == PredictionModel.transaction_id
    ).filter(TransactionModel.id == transaction_id).first()

    if not result:
        return None

    tx, pred = result

    raw_dict = {
        "Timestamp": str(tx.timestamp),
        "From Bank": tx.from_bank,
        "Account": tx.account,
        "To Bank": tx.to_bank,
        "Account.1": tx.receiver_account,
        "Amount Received": tx.amount_received,
        "Receiving Currency": tx.receiving_currency,
        "Amount Paid": tx.amount_paid,
        "Payment Currency": tx.payment_currency,
        "Payment Format": tx.payment_format,
    }

    feature_df = build_raw_feature_df(raw_dict)
    engineered_features = feature_df.to_dict(orient="records")[0]

    return {
        "transaction": {
            "id": tx.id,
            "timestamp": str(tx.timestamp),
            "from_bank": tx.from_bank,
            "account": tx.account,
            "to_bank": tx.to_bank,
            "receiver_account": tx.receiver_account,
            "amount_received": tx.amount_received,
            "amount_paid": tx.amount_paid,
            "receiving_currency": tx.receiving_currency,
            "payment_currency": tx.payment_currency,
            "payment_format": tx.payment_format,
            "created_at": tx.created_at,
        },
        "model_result": {
            "prediction": pred.prediction,
            "label": "Suspicious" if pred.prediction == 1 else "Normal",
            "probability": pred.probability,
            "threshold": pred.threshold,
            "risk_level": pred.risk_level,
            "model_name": pred.model_name,
            "model_version": pred.model_version,
        },
        "engineered_features": engineered_features,
    }
