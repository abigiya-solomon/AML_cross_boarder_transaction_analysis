from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class TransactionModel(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=utc_now, index=True)
    from_bank = Column(Integer, nullable=False, index=True)
    account = Column(String(64), nullable=False, index=True)
    to_bank = Column(Integer, nullable=False, index=True)
    receiver_account = Column(String(64), nullable=False, index=True)
    amount_received = Column(Float, nullable=False)
    amount_paid = Column(Float, nullable=False)
    receiving_currency = Column(String(32), nullable=False)
    payment_currency = Column(String(32), nullable=False)
    payment_format = Column(String(32), nullable=False)
    created_at = Column(DateTime, default=utc_now)

    prediction = relationship("PredictionModel", back_populates="transaction", uselist=False, cascade="all, delete-orphan")

class PredictionModel(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False, unique=True, index=True)
    probability = Column(Float, nullable=False)
    prediction = Column(Integer, nullable=False)
    risk_level = Column(String(16), nullable=False)
    threshold = Column(Float, default=0.50)
    model_name = Column(String(32), default="LightGBM")
    model_version = Column(String(16), default="1.0")
    created_at = Column(DateTime, default=utc_now)

    transaction = relationship("TransactionModel", back_populates="prediction")

class UploadModel(Base):
    __tablename__ = "uploads"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    row_count = Column(Integer, default=0)
    processed_count = Column(Integer, default=0)
    suspicious_count = Column(Integer, default=0)
    status = Column(String(32), default="completed")
    created_at = Column(DateTime, default=utc_now)
