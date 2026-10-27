from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class TransactionBase(BaseModel):
    timestamp: Optional[str] = Field(None, json_schema_extra={"example": "2022-09-21 12:30:00"})
    from_bank: int = Field(..., json_schema_extra={"example": 20})
    account: str = Field(..., json_schema_extra={"example": "100234"})
    to_bank: int = Field(..., json_schema_extra={"example": 3196})
    receiver_account: str = Field(..., json_schema_extra={"example": "884129"})
    amount_received: float = Field(..., ge=0.0, json_schema_extra={"example": 15000.0})
    receiving_currency: str = Field(..., json_schema_extra={"example": "US Dollar"})
    amount_paid: float = Field(..., ge=0.0, json_schema_extra={"example": 15000.0})
    payment_currency: str = Field(..., json_schema_extra={"example": "US Dollar"})
    payment_format: str = Field(..., json_schema_extra={"example": "Wire"})

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
