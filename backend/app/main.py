import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.db.database import Base, engine, SessionLocal
from app.db.models import TransactionModel, PredictionModel
from app.ml.model_loader import model_loader
from app.api.routes import health, predictions, transactions, dashboard, model_info

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure tables are created
Base.metadata.create_all(bind=engine)

def seed_sample_data():
    """Populates initial sample transactions if database is fresh."""
    db = SessionLocal()
    try:
        count = db.query(TransactionModel).count()
        if count == 0:
            logger.info("Seeding initial AML sample transactions...")
            from app.services.prediction_service import create_single_prediction
            
            sample_txs = [
                {
                    "timestamp": "2022-09-21 02:14:00",
                    "from_bank": 20,
                    "account": "100234",
                    "to_bank": 3196,
                    "receiver_account": "884129",
                    "amount_received": 950000.0,
                    "receiving_currency": "US Dollar",
                    "amount_paid": 950000.0,
                    "payment_currency": "US Dollar",
                    "payment_format": "Wire"
                },
                {
                    "timestamp": "2022-09-21 09:30:15",
                    "from_bank": 114,
                    "account": "551290",
                    "to_bank": 114,
                    "receiver_account": "772109",
                    "amount_received": 1200.0,
                    "receiving_currency": "Euro",
                    "amount_paid": 1200.0,
                    "payment_currency": "Euro",
                    "payment_format": "ACH"
                },
                {
                    "timestamp": "2022-09-22 23:45:10",
                    "from_bank": 303,
                    "account": "992110",
                    "to_bank": 287,
                    "receiver_account": "441201",
                    "amount_received": 450000.0,
                    "receiving_currency": "Bitcoin",
                    "amount_paid": 450000.0,
                    "payment_currency": "Bitcoin",
                    "payment_format": "Bitcoin"
                },
                {
                    "timestamp": "2022-09-23 14:10:00",
                    "from_bank": 12,
                    "account": "332019",
                    "to_bank": 15,
                    "receiver_account": "881290",
                    "amount_received": 4500.0,
                    "receiving_currency": "UK Pound",
                    "amount_paid": 4500.0,
                    "payment_currency": "UK Pound",
                    "payment_format": "Credit Card"
                },
                {
                    "timestamp": "2022-09-24 03:22:00",
                    "from_bank": 3314,
                    "account": "664120",
                    "to_bank": 20,
                    "receiver_account": "119823",
                    "amount_received": 880000.0,
                    "receiving_currency": "US Dollar",
                    "amount_paid": 880000.0,
                    "payment_currency": "US Dollar",
                    "payment_format": "Wire"
                }
            ]
            for tx in sample_txs:
                create_single_prediction(tx, db)
            logger.info("Sample transaction seeding complete.")
    except Exception as e:
        logger.warning(f"Sample data seeding skipped: {e}")
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load ML artifacts
    try:
        model_loader.load()
        logger.info("ML Model and preprocessor loaded successfully on startup.")
    except Exception as e:
        logger.error(f"Failed to load ML artifacts at startup: {e}")
    
    seed_sample_data()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Cross-Border Transaction Analysis and Anti-Money Laundering (AML) Risk Prediction Service",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if settings.CORS_ORIGINS != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(health.router, prefix=settings.API_V1_STR)
app.include_router(predictions.router, prefix=settings.API_V1_STR)
app.include_router(transactions.router, prefix=settings.API_V1_STR)
app.include_router(dashboard.router, prefix=settings.API_V1_STR)
app.include_router(model_info.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "message": "AML Cross-Border Transaction Analysis API is running.",
        "docs_url": "/docs",
        "health_url": f"{settings.API_V1_STR}/health"
    }
