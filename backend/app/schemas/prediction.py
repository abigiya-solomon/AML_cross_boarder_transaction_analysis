from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List
from app.schemas.transaction import TransactionBase, TransactionResponse

class SinglePredictionRequest(TransactionBase):
    pass

class PredictionResponse(BaseModel):
    transaction_id: Optional[int] = None
    probability: float
    prediction: int  # 0: Normal, 1: Suspicious
    threshold: float
    label: str  # "Normal" or "Suspicious"
    risk_level: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    model_name: str
    model_version: str
    engineered_features: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)

class TransactionWithPredictionResponse(TransactionResponse):
    probability: float
    prediction: int
    label: str
    risk_level: str

class PaginatedTransactionsResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[TransactionWithPredictionResponse]

class BatchUploadResponse(BaseModel):
    filename: str
    total_rows: int
    processed_count: int
    suspicious_count: int
    suspicious_rate: float
    message: str
