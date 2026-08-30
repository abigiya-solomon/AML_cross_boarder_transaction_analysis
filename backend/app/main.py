import os
import pandas as pd
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.db.database import engine, Base, SessionLocal
from app.db.models import TransactionModel, PredictionModel
from app.ml.model_loader import model_loader
from app.ml.inference import predict_single_transaction

from app.api.routes import health, predictions, transactions, dashboard, model_info

# Initialize tables automatically upon app load
Base.metadata.create_all(bind=engine)

def seed_sample_data():
    db = SessionLocal()
    try:
        count = db.query(TransactionModel).count()
        if count == 0:
            print("Seeding initial sample AML transaction data into database...")
            sample_txs = [
                {"timestamp": "2022-09-21 12:30:00", "from_bank": 20, "account": "100234", "to_bank": 3196, "receiver_account": "884129", "amount_received": 14500.0, "receiving_currency": "US Dollar", "amount_paid": 14500.0, "payment_currency": "US Dollar", "payment_format": "Wire"},
                {"timestamp": "2022-09-21 14:15:22", "from_bank": 115, "account": "339104", "to_bank": 20, "receiver_account": "100234", "amount_received": 8900.0, "receiving_currency": "US Dollar", "amount_paid": 8900.0, "payment_currency": "US Dollar", "payment_format": "ACH"},
                {"timestamp": "2022-09-22 02:45:10", "from_bank": 9041, "account": "992014", "to_bank": 8812, "receiver_account": "771029", "amount_received": 250000.0, "receiving_currency": "UK Pound", "amount_paid": 250000.0, "payment_currency": "UK Pound", "payment_format": "Wire"},
                {"timestamp": "2022-09-22 03:10:05", "from_bank": 9041, "account": "992014", "to_bank": 4410, "receiver_account": "119023", "amount_received": 180000.0, "receiving_currency": "UK Pound", "amount_paid": 180000.0, "payment_currency": "UK Pound", "payment_format": "Wire"},
                {"timestamp": "2022-09-22 09:30:00", "from_bank": 45, "account": "500112", "to_bank": 45, "receiver_account": "600981", "amount_received": 120.0, "receiving_currency": "Euro", "amount_paid": 120.0, "payment_currency": "Euro", "payment_format": "Credit Card"},
                {"timestamp": "2022-09-23 11:20:45", "from_bank": 300, "account": "440192", "to_bank": 800, "receiver_account": "331092", "amount_received": 4500.0, "receiving_currency": "Canadian Dollar", "amount_paid": 4500.0, "payment_currency": "Canadian Dollar", "payment_format": "Cheque"},
                {"timestamp": "2022-09-23 23:55:00", "from_bank": 7712, "account": "882103", "to_bank": 9901, "receiver_account": "441029", "amount_received": 95000.0, "receiving_currency": "Bitcoin", "amount_paid": 95000.0, "payment_currency": "Bitcoin", "payment_format": "Bitcoin"},
                {"timestamp": "2022-09-24 01:15:30", "from_bank": 7712, "account": "882103", "to_bank": 1120, "receiver_account": "550192", "amount_received": 120000.0, "receiving_currency": "Bitcoin", "amount_paid": 120000.0, "payment_currency": "Bitcoin", "payment_format": "Bitcoin"},
                {"timestamp": "2022-09-24 16:40:00", "from_bank": 12, "account": "100994", "to_bank": 12, "receiver_account": "200118", "amount_received": 350.0, "receiving_currency": "US Dollar", "amount_paid": 350.0, "payment_currency": "US Dollar", "payment_format": "Cash"},
                {"timestamp": "2022-09-25 10:05:12", "from_bank": 505, "account": "771004", "to_bank": 606, "receiver_account": "882019", "amount_received": 32000.0, "receiving_currency": "Swiss Franc", "amount_paid": 32000.0, "payment_currency": "Swiss Franc", "payment_format": "Wire"},
            ]
            for tx_data in sample_txs:
                ts_val = pd.to_datetime(tx_data["timestamp"]).to_pydatetime()
                tx_model = TransactionModel(
                    timestamp=ts_val,
                    from_bank=tx_data["from_bank"],
                    account=tx_data["account"],
                    to_bank=tx_data["to_bank"],
                    receiver_account=tx_data["receiver_account"],
                    amount_received=tx_data["amount_received"],
                    amount_paid=tx_data["amount_paid"],
                    receiving_currency=tx_data["receiving_currency"],
                    payment_currency=tx_data["payment_currency"],
                    payment_format=tx_data["payment_format"],
                )
                db.add(tx_model)
                db.flush()

                raw_inf = {
                    "Timestamp": tx_data["timestamp"],
                    "From Bank": tx_data["from_bank"],
                    "Account": tx_data["account"],
                    "To Bank": tx_data["to_bank"],
                    "Account.1": tx_data["receiver_account"],
                    "Amount Received": tx_data["amount_received"],
                    "Receiving Currency": tx_data["receiving_currency"],
                    "Amount Paid": tx_data["amount_paid"],
                    "Payment Currency": tx_data["payment_currency"],
                    "Payment Format": tx_data["payment_format"],
                }
                res = predict_single_transaction(raw_inf)
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

            db.commit()
            print("Successfully seeded 10 sample transactions and predictions.")
    except Exception as e:
        print("Error seeding sample data:", e)
        db.rollback()
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading ML artifacts on startup...")

    try:
        model_loader.load_artifacts()
        print("ML MODEL LOADED SUCCESSFULLY")
    except Exception as e:
        print(f"ML MODEL LOAD ERROR: {type(e).__name__}: {e}")

    try:
        seed_sample_data()
        print("DATABASE SEEDING COMPLETED")
    except Exception as e:
        print(f"DATABASE SEEDING ERROR: {type(e).__name__}: {e}")

    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix=settings.API_PREFIX, tags=["Health"])
app.include_router(predictions.router, prefix=settings.API_PREFIX, tags=["Predictions"])
app.include_router(transactions.router, prefix=settings.API_PREFIX, tags=["Transactions"])
app.include_router(dashboard.router, prefix=settings.API_PREFIX, tags=["Dashboard"])
app.include_router(model_info.router, prefix=settings.API_PREFIX, tags=["Model Info"])

@app.get("/")
def root():
    return {
        "title": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "health": f"{settings.API_PREFIX}/health"
    }
