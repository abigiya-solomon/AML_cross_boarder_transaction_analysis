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

class DistributionItem(BaseModel):
    name: str
    value: int
    suspicious_count: int = 0
    suspicious_rate: float = 0.0

class EntityRiskItem(BaseModel):
    id: str
    count: int
    suspicious_count: int
    suspicious_rate: float

class DashboardStatsResponse(BaseModel):
    kpis: KPICards
    suspicious_over_time: List[TimeSeriesPoint]
    volume_over_time: List[TimeSeriesPoint]
    risk_distribution: List[DistributionItem]
    payment_format_distribution: List[DistributionItem]
    currency_distribution: List[DistributionItem]
    top_suspicious_accounts: List[EntityRiskItem]
    top_suspicious_banks: List[EntityRiskItem]
