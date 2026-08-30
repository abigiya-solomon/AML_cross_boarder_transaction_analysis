from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from app.schemas.transaction import TransactionResponse

class PredictionResponse(BaseModel):
    id: Optional[int] = None
    transaction_id: Optional[int] = None
    prediction: int = Field(..., description="0 for Normal, 1 for Suspicious")
    label: str = Field(..., description="'Normal' or 'Suspicious'")
    probability: float = Field(..., description="Suspicious transaction probability [0.0 - 1.0]")
    threshold: float = Field(default=0.50)
    risk_level: str = Field(..., description="'LOW', 'MEDIUM', 'HIGH', or 'CRITICAL'")
    model_name: str = Field(default="LightGBM")
    model_version: str = Field(default="1.0")
    engineered_features: Optional[Dict[str, Any]] = None
    transaction: Optional[TransactionResponse] = None

class SinglePredictionRequest(BaseModel):
    timestamp: str = Field(..., json_schema_extra={"example": "2022-09-21 12:30:00"})
    from_bank: int = Field(..., json_schema_extra={"example": 123})
    account: str = Field(..., json_schema_extra={"example": "456789"})
    to_bank: int = Field(..., json_schema_extra={"example": 987})
    receiver_account: str = Field(..., json_schema_extra={"example": "123456"})
    amount_received: float = Field(..., json_schema_extra={"example": 10000.0})
    receiving_currency: str = Field(..., json_schema_extra={"example": "US Dollar"})
    amount_paid: float = Field(..., json_schema_extra={"example": 10000.0})
    payment_currency: str = Field(..., json_schema_extra={"example": "US Dollar"})
    payment_format: str = Field(..., json_schema_extra={"example": "Wire"})

class BatchUploadResponse(BaseModel):
    upload_id: int
    filename: str
    total_rows: int
    processed_count: int
    suspicious_count: int
    suspicious_rate: float
    status: str
