from pydantic import BaseModel
from typing import List, Dict, Any

class KPICards(BaseModel):
    total_transactions: int
    suspicious_transactions: int
    suspicious_rate: float
    average_risk_probability: float
    high_risk_transactions: int

class TimeSeriesPoint(BaseModel):
    date: str
    total: int
    suspicious: int

class CategoryDistribution(BaseModel):
    name: str
    value: int
    suspicious_count: int

class TopAccountMetric(BaseModel):
    account_key: str
    transaction_count: int
    suspicious_count: int
    total_amount: float

class TopBankMetric(BaseModel):
    bank_id: int
    transaction_count: int
    suspicious_count: int

class DashboardStatsResponse(BaseModel):
    kpis: KPICards
    suspicious_over_time: List[TimeSeriesPoint]
    volume_over_time: List[TimeSeriesPoint]
    payment_format_distribution: List[CategoryDistribution]
    currency_distribution: List[CategoryDistribution]
    risk_distribution: List[Dict[str, Any]]
    top_suspicious_accounts: List[TopAccountMetric]
    top_suspicious_banks: List[TopBankMetric]
