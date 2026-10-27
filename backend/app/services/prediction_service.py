import json
import io
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.models import TransactionModel, PredictionModel, UploadModel
from app.ml.inference import predict_transaction
from app.schemas.prediction import PredictionResponse, BatchUploadResponse

def create_single_prediction(transaction_data: dict, db: Session) -> dict:
    # 1. Run inference
    inference_result = predict_transaction(transaction_data)

    # 2. Store transaction in DB
    tx_timestamp = None
    if transaction_data.get("timestamp"):
        try:
            tx_timestamp = datetime.strptime(transaction_data["timestamp"], "%Y-%m-%d %H:%M:%S")
        except Exception:
            tx_timestamp = datetime.utcnow()
    else:
        tx_timestamp = datetime.utcnow()

    tx = TransactionModel(
        timestamp=tx_timestamp,
        from_bank=transaction_data["from_bank"],
        account=str(transaction_data["account"]),
        to_bank=transaction_data["to_bank"],
        receiver_account=str(transaction_data["receiver_account"]),
        amount_received=float(transaction_data["amount_received"]),
        amount_paid=float(transaction_data["amount_paid"]),
        receiving_currency=str(transaction_data["receiving_currency"]),
        payment_currency=str(transaction_data["payment_currency"]),
        payment_format=str(transaction_data["payment_format"]),
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)

    # 3. Store prediction in DB
    pred = PredictionModel(
        transaction_id=tx.id,
        probability=inference_result["probability"],
        prediction=inference_result["prediction"],
        threshold=inference_result["threshold"],
        label=inference_result["label"],
        risk_level=inference_result["risk_level"],
        model_name=inference_result["model_name"],
        model_version=inference_result["model_version"],
        engineered_features=json.dumps(inference_result.get("engineered_features", {})),
    )
    db.add(pred)
    db.commit()
    db.refresh(pred)

    inference_result["transaction_id"] = tx.id
    return inference_result

def process_batch_csv(file_contents: bytes, filename: str, db: Session) -> BatchUploadResponse:
    df = pd.read_csv(io.BytesIO(file_contents))
    
    # Standardize column mappings if needed
    col_mapping = {
        "Account.1": "receiver_account",
        "To Account": "receiver_account",
        "From Bank": "from_bank",
        "To Bank": "to_bank",
        "Account": "account",
        "Amount Received": "amount_received",
        "Amount Paid": "amount_paid",
        "Receiving Currency": "receiving_currency",
        "Payment Currency": "payment_currency",
        "Payment Format": "payment_format",
        "Timestamp": "timestamp"
    }
    df = df.rename(columns=col_mapping)

    total_rows = len(df)
    processed_count = 0
    suspicious_count = 0

    for _, row in df.iterrows():
        tx_dict = {
            "timestamp": str(row.get("timestamp", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))),
            "from_bank": int(row["from_bank"]),
            "account": str(row["account"]),
            "to_bank": int(row["to_bank"]),
            "receiver_account": str(row["receiver_account"]),
            "amount_received": float(row["amount_received"]),
            "amount_paid": float(row["amount_paid"]),
            "receiving_currency": str(row["receiving_currency"]),
            "payment_currency": str(row["payment_currency"]),
            "payment_format": str(row["payment_format"]),
        }
        res = create_single_prediction(tx_dict, db)
        processed_count += 1
        if res["prediction"] == 1:
            suspicious_count += 1

    suspicious_rate = round((suspicious_count / processed_count * 100), 2) if processed_count > 0 else 0.0

    upload_rec = UploadModel(
        filename=filename,
        total_rows=total_rows,
        processed_count=processed_count,
        suspicious_count=suspicious_count,
        suspicious_rate=suspicious_rate,
    )
    db.add(upload_rec)
    db.commit()

    return BatchUploadResponse(
        filename=filename,
        total_rows=total_rows,
        processed_count=processed_count,
        suspicious_count=suspicious_count,
        suspicious_rate=suspicious_rate,
        message=f"Successfully processed {processed_count} transactions with {suspicious_count} suspicious alerts flagged."
    )
