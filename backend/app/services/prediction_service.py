from datetime import datetime, timezone
import pandas as pd
from sqlalchemy.orm import Session
from app.db.models import TransactionModel, PredictionModel, UploadModel
from app.ml.inference import predict_single_transaction, predict_batch_df

def process_single_prediction(db: Session, raw_tx_dict: dict) -> dict:
    ts_str = str(raw_tx_dict.get("timestamp", raw_tx_dict.get("Timestamp", "2022-09-21 12:30:00")))
    try:
        ts_val = pd.to_datetime(ts_str).to_pydatetime()
    except Exception:
        ts_val = datetime.now(timezone.utc)

    tx_model = TransactionModel(
        timestamp=ts_val,
        from_bank=int(raw_tx_dict["from_bank"] if "from_bank" in raw_tx_dict else raw_tx_dict["From Bank"]),
        account=str(raw_tx_dict["account"] if "account" in raw_tx_dict else raw_tx_dict["Account"]),
        to_bank=int(raw_tx_dict["to_bank"] if "to_bank" in raw_tx_dict else raw_tx_dict["To Bank"]),
        receiver_account=str(raw_tx_dict["receiver_account"] if "receiver_account" in raw_tx_dict else raw_tx_dict["Account.1"]),
        amount_received=float(raw_tx_dict["amount_received"] if "amount_received" in raw_tx_dict else raw_tx_dict["Amount Received"]),
        amount_paid=float(raw_tx_dict["amount_paid"] if "amount_paid" in raw_tx_dict else raw_tx_dict["Amount Paid"]),
        receiving_currency=str(raw_tx_dict["receiving_currency"] if "receiving_currency" in raw_tx_dict else raw_tx_dict["Receiving Currency"]),
        payment_currency=str(raw_tx_dict["payment_currency"] if "payment_currency" in raw_tx_dict else raw_tx_dict["Payment Currency"]),
        payment_format=str(raw_tx_dict["payment_format"] if "payment_format" in raw_tx_dict else raw_tx_dict["Payment Format"]),
    )
    db.add(tx_model)
    db.commit()
    db.refresh(tx_model)

    raw_inference_dict = {
        "Timestamp": ts_str,
        "From Bank": tx_model.from_bank,
        "Account": tx_model.account,
        "To Bank": tx_model.to_bank,
        "Account.1": tx_model.receiver_account,
        "Amount Received": tx_model.amount_received,
        "Receiving Currency": tx_model.receiving_currency,
        "Amount Paid": tx_model.amount_paid,
        "Payment Currency": tx_model.payment_currency,
        "Payment Format": tx_model.payment_format,
    }

    pred_res = predict_single_transaction(raw_inference_dict)

    pred_model = PredictionModel(
        transaction_id=tx_model.id,
        probability=pred_res["probability"],
        prediction=pred_res["prediction"],
        risk_level=pred_res["risk_level"],
        threshold=pred_res["threshold"],
        model_name=pred_res["model_name"],
        model_version=pred_res["model_version"],
    )
    db.add(pred_model)
    db.commit()
    db.refresh(pred_model)

    pred_res["id"] = pred_model.id
    pred_res["transaction_id"] = tx_model.id
    pred_res["transaction"] = {
        "id": tx_model.id,
        "timestamp": str(tx_model.timestamp),
        "from_bank": tx_model.from_bank,
        "account": tx_model.account,
        "to_bank": tx_model.to_bank,
        "receiver_account": tx_model.receiver_account,
        "amount_received": tx_model.amount_received,
        "amount_paid": tx_model.amount_paid,
        "receiving_currency": tx_model.receiving_currency,
        "payment_currency": tx_model.payment_currency,
        "payment_format": tx_model.payment_format,
        "created_at": tx_model.created_at,
    }
    return pred_res

def process_batch_upload(db: Session, filename: str, df: pd.DataFrame) -> dict:
    upload_rec = UploadModel(
        filename=filename,
        row_count=len(df),
        processed_count=0,
        suspicious_count=0,
        status="processing"
    )
    db.add(upload_rec)
    db.commit()
    db.refresh(upload_rec)

    batch_size = 500
    total_processed = 0
    suspicious_count = 0

    for i in range(0, len(df), batch_size):
        chunk = df.iloc[i : i + batch_size]
        results = predict_batch_df(chunk)

        for tx_dict, res in results:
            ts_str = tx_dict["Timestamp"]
            try:
                ts_val = pd.to_datetime(ts_str).to_pydatetime()
            except Exception:
                ts_val = datetime.now(timezone.utc)

            tx_model = TransactionModel(
                timestamp=ts_val,
                from_bank=tx_dict["From Bank"],
                account=tx_dict["Account"],
                to_bank=tx_dict["To Bank"],
                receiver_account=tx_dict["Account.1"],
                amount_received=tx_dict["Amount Received"],
                amount_paid=tx_dict["Amount Paid"],
                receiving_currency=tx_dict["Receiving Currency"],
                payment_currency=tx_dict["Payment Currency"],
                payment_format=tx_dict["Payment Format"],
            )
            db.add(tx_model)
            db.flush()

            pred_model = PredictionModel(
                transaction_id=tx_model.id,
                probability=res["probability"],
                prediction=res["prediction"],
                risk_level=res["risk_level"],
                threshold=res["threshold"],
                model_name=res["model_name"],
                model_version=res["model_version"],
            )
            db.add(pred_model)

            total_processed += 1
            if res["prediction"] == 1:
                suspicious_count += 1

        db.commit()

    upload_rec.processed_count = total_processed
    upload_rec.suspicious_count = suspicious_count
    upload_rec.status = "completed"
    db.commit()

    rate = round((suspicious_count / total_processed * 100), 2) if total_processed > 0 else 0.0

    return {
        "upload_id": upload_rec.id,
        "filename": filename,
        "total_rows": len(df),
        "processed_count": total_processed,
        "suspicious_count": suspicious_count,
        "suspicious_rate": rate,
        "status": "completed",
    }
