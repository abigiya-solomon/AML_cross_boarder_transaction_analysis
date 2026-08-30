from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class TransactionBase(BaseModel):
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

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
