from collections import defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models import TransactionModel, PredictionModel
from app.schemas.dashboard import (
    DashboardStatsResponse,
    KPICards,
    TimeSeriesPoint,
    CategoryDistribution,
    TopAccountMetric,
    TopBankMetric,
)

def get_dashboard_statistics(db: Session) -> DashboardStatsResponse:
    total_tx = db.query(TransactionModel).count()
    suspicious_tx = db.query(PredictionModel).filter(PredictionModel.prediction == 1).count()
    suspicious_rate = round((suspicious_tx / total_tx * 100), 2) if total_tx > 0 else 0.0

    avg_prob = db.query(func.avg(PredictionModel.probability)).scalar() or 0.0
    high_risk_count = db.query(PredictionModel).filter(PredictionModel.probability >= 0.70).count()

    kpis = KPICards(
        total_transactions=total_tx,
        suspicious_transactions=suspicious_tx,
        suspicious_rate=suspicious_rate,
        average_risk_probability=round(float(avg_prob), 4),
        high_risk_transactions=high_risk_count,
    )

    # Time series grouping by date
    all_records = (
        db.query(TransactionModel.timestamp, PredictionModel.prediction)
        .join(PredictionModel, TransactionModel.id == PredictionModel.transaction_id)
        .all()
    )

    daily_total = defaultdict(int)
    daily_suspicious = defaultdict(int)

    for ts, pred in all_records:
        date_str = ts.strftime("%Y-%m-%d") if ts else "Unknown"
        daily_total[date_str] += 1
        if pred == 1:
            daily_suspicious[date_str] += 1

    sorted_dates = sorted(daily_total.keys())
    time_series = [
        TimeSeriesPoint(
            date=d,
            total=daily_total[d],
            suspicious=daily_suspicious[d]
        )
        for d in sorted_dates
    ]

    # Payment format distribution
    format_counts = (
        db.query(
            TransactionModel.payment_format,
            func.count(TransactionModel.id),
            func.sum(PredictionModel.prediction)
        )
        .join(PredictionModel, TransactionModel.id == PredictionModel.transaction_id)
        .group_by(TransactionModel.payment_format)
        .all()
    )
    payment_format_dist = [
        CategoryDistribution(
            name=fmt,
            value=count,
            suspicious_count=int(susp or 0)
        )
        for fmt, count, susp in format_counts
    ]

    # Currency distribution
    currency_counts = (
        db.query(
            TransactionModel.receiving_currency,
            func.count(TransactionModel.id),
            func.sum(PredictionModel.prediction)
        )
        .join(PredictionModel, TransactionModel.id == PredictionModel.transaction_id)
        .group_by(TransactionModel.receiving_currency)
        .all()
    )
    currency_dist = [
        CategoryDistribution(
            name=curr,
            value=count,
            suspicious_count=int(susp or 0)
        )
        for curr, count, susp in currency_counts
    ]

    # Risk level distribution
    risk_counts = (
        db.query(PredictionModel.risk_level, func.count(PredictionModel.id))
        .group_by(PredictionModel.risk_level)
        .all()
    )
    risk_dist = [{"name": r_level, "value": count} for r_level, count in risk_counts]

    # Top suspicious accounts
    top_accounts_raw = (
        db.query(
            TransactionModel.from_bank,
            TransactionModel.account,
            func.count(TransactionModel.id).label("tx_cnt"),
            func.sum(PredictionModel.prediction).label("susp_cnt"),
            func.sum(TransactionModel.amount_paid).label("tot_amt")
        )
        .join(PredictionModel, TransactionModel.id == PredictionModel.transaction_id)
        .group_by(TransactionModel.from_bank, TransactionModel.account)
        .order_by(func.sum(PredictionModel.prediction).desc())
        .limit(5)
        .all()
    )
    top_accounts = [
        TopAccountMetric(
            account_key=f"{b}_{a}",
            transaction_count=t_cnt,
            suspicious_count=int(s_cnt or 0),
            total_amount=round(float(amt or 0), 2)
        )
        for b, a, t_cnt, s_cnt, amt in top_accounts_raw
    ]

    # Top suspicious banks
    top_banks_raw = (
        db.query(
            TransactionModel.from_bank,
            func.count(TransactionModel.id).label("tx_cnt"),
            func.sum(PredictionModel.prediction).label("susp_cnt")
        )
        .join(PredictionModel, TransactionModel.id == PredictionModel.transaction_id)
        .group_by(TransactionModel.from_bank)
        .order_by(func.sum(PredictionModel.prediction).desc())
        .limit(5)
        .all()
    )
    top_banks = [
        TopBankMetric(
            bank_id=b,
            transaction_count=t_cnt,
            suspicious_count=int(s_cnt or 0)
        )
        for b, t_cnt, s_cnt in top_banks_raw
    ]

    return DashboardStatsResponse(
        kpis=kpis,
        suspicious_over_time=time_series,
        volume_over_time=time_series,
        payment_format_distribution=payment_format_dist,
        currency_distribution=currency_dist,
        risk_distribution=risk_dist,
        top_suspicious_accounts=top_accounts,
        top_suspicious_banks=top_banks,
    )
