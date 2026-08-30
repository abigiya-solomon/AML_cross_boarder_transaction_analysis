from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.dashboard import DashboardStatsResponse
from app.services.dashboard_service import get_dashboard_statistics

router = APIRouter()

@router.get("/dashboard/stats", response_model=DashboardStatsResponse)
def get_dashboard_stats(db: Session = Depends(get_db)):
    return get_dashboard_statistics(db)
