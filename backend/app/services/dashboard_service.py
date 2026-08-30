from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.db.models import TransactionModel, PredictionModel

def get_dashboard_statistics(db: Session) -> dict:
    total_transactions = db.query(func.count(TransactionModel.id)).scalar() or 0
    suspicious_transactions = db.query(func.count(PredictionModel.id)).filter(PredictionModel.prediction == 1).scalar() or 0
    suspicious_rate = round((suspicious_transactions / total_transactions * 100), 2) if total_transactions > 0 else 0.0

    avg_prob = db.query(func.avg(PredictionModel.probability)).scalar() or 0.0
    high_risk_count = db.query(func.count(PredictionModel.id)).filter(
        PredictionModel.risk_level.in_(["HIGH", "CRITICAL"])
    ).scalar() or 0

    kpis = {
        "total_transactions": total_transactions,
        "suspicious_transactions": suspicious_transactions,
        "suspicious_rate": suspicious_rate,
        "average_risk_probability": round(float(avg_prob), 4),
        "high_risk_transactions": high_risk_count,
    }

    # Time series (by date)
    date_col = func.date(TransactionModel.timestamp)
    ts_query = db.query(
        date_col.label("date"),
        func.count(TransactionModel.id).label("total"),
        func.sum(PredictionModel.prediction).label("suspicious")
    ).join(
        PredictionModel, TransactionModel.id == PredictionModel.transaction_id
    ).group_by(date_col).order_by(date_col).all()

    suspicious_over_time = []
    volume_over_time = []
    for date_str, total, susp in ts_query:
        s_val = int(susp or 0)
        t_val = int(total or 0)
        d_str = str(date_str) if date_str else "Unknown"
        suspicious_over_time.append({"date": d_str, "total": t_val, "suspicious": s_val})
        volume_over_time.append({"date": d_str, "total": t_val, "suspicious": s_val})

    # Risk level distribution
    risk_query = db.query(
        PredictionModel.risk_level.label("risk"),
        func.count(PredictionModel.id).label("count")
    ).group_by(PredictionModel.risk_level).all()

    risk_map = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
    for risk, count in risk_query:
        if risk in risk_map:
            risk_map[risk] = count

    risk_distribution = [
        {"name": k, "value": v, "suspicious_count": v if k in ["HIGH", "CRITICAL"] else 0, "suspicious_rate": round(v/total_transactions*100, 2) if total_transactions > 0 else 0}
        for k, v in risk_map.items()
    ]

    # Payment format distribution
    fmt_query = db.query(
        TransactionModel.payment_format.label("fmt"),
        func.count(TransactionModel.id).label("total"),
        func.sum(PredictionModel.prediction).label("suspicious")
    ).join(
        PredictionModel, TransactionModel.id == PredictionModel.transaction_id
    ).group_by(TransactionModel.payment_format).all()

    fmt_distribution = []
    for fmt, total, susp in fmt_query:
        t = int(total or 0)
        s = int(susp or 0)
        r = round((s / t * 100), 2) if t > 0 else 0.0
        fmt_distribution.append({
            "name": str(fmt),
            "value": t,
            "suspicious_count": s,
            "suspicious_rate": r,
        })

    # Currency distribution
    curr_query = db.query(
        TransactionModel.receiving_currency.label("curr"),
        func.count(TransactionModel.id).label("total"),
        func.sum(PredictionModel.prediction).label("suspicious")
    ).join(
        PredictionModel, TransactionModel.id == PredictionModel.transaction_id
    ).group_by(TransactionModel.receiving_currency).all()

    curr_distribution = []
    for curr, total, susp in curr_query:
        t = int(total or 0)
        s = int(susp or 0)
        r = round((s / t * 100), 2) if t > 0 else 0.0
        curr_distribution.append({
            "name": str(curr),
            "value": t,
            "suspicious_count": s,
            "suspicious_rate": r,
        })

    # Top suspicious accounts
    account_query = db.query(
        TransactionModel.account.label("acc"),
        func.count(TransactionModel.id).label("total"),
        func.sum(PredictionModel.prediction).label("suspicious")
    ).join(
        PredictionModel, TransactionModel.id == PredictionModel.transaction_id
    ).group_by(TransactionModel.account).order_by(desc("suspicious")).limit(10).all()

    top_accounts = []
    for acc, total, susp in account_query:
        t = int(total or 0)
        s = int(susp or 0)
        r = round((s / t * 100), 2) if t > 0 else 0.0
        top_accounts.append({
            "id": f"Account {acc}",
            "count": t,
            "suspicious_count": s,
            "suspicious_rate": r,
        })

    # Top suspicious banks
    bank_query = db.query(
        TransactionModel.from_bank.label("bank"),
        func.count(TransactionModel.id).label("total"),
        func.sum(PredictionModel.prediction).label("suspicious")
    ).join(
        PredictionModel, TransactionModel.id == PredictionModel.transaction_id
    ).group_by(TransactionModel.from_bank).order_by(desc("suspicious")).limit(10).all()

    top_banks = []
    for bank, total, susp in bank_query:
        t = int(total or 0)
        s = int(susp or 0)
        r = round((s / t * 100), 2) if t > 0 else 0.0
        top_banks.append({
            "id": f"Bank {bank}",
            "count": t,
            "suspicious_count": s,
            "suspicious_rate": r,
        })

    return {
        "kpis": kpis,
        "suspicious_over_time": suspicious_over_time,
        "volume_over_time": volume_over_time,
        "risk_distribution": risk_distribution,
        "payment_format_distribution": fmt_distribution,
        "currency_distribution": curr_distribution,
        "top_suspicious_accounts": top_accounts,
        "top_suspicious_banks": top_banks,
    }
