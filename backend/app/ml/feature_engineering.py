import numpy as np
import pandas as pd

MODEL_NUMERIC_FEATURES = [
    "Amount Received",
    "Amount Paid",
    "Sender_Transaction_Count",
    "Sender_Total_Amount",
    "Sender_Max_Amount",
    "Sender_Average_Amount",
    "Sender_Unique_Receivers",
    "Sender_Unique_Days",
    "Sender_Active_Hours",
    "Sender_Weekend_Transactions",
    "Sender_Night_Transactions",
    "Sender_Average_Daily_Transactions",
    "Receiver_Transaction_Count",
    "Receiver_Total_Amount",
    "Receiver_Max_Amount",
    "Receiver_Average_Amount",
    "Receiver_Unique_Senders",
    "Receiver_Unique_Days",
    "Receiver_Active_Hours",
    "Receiver_Weekend_Transactions",
    "Receiver_Night_Transactions",
    "Receiver_Average_Daily_Transactions",
    "Relationship_Transaction_Count",
    "Relationship_Total_Amount",
    "Relationship_Max_Amount",
    "Relationship_Average_Amount",
    "Hour",
    "Day",
    "DayOfWeek",
    "IsWeekend",
    "IsNight",
    "Amount_Difference",
    "Amount_Absolute_Difference",
    "Amount_Ratio",
    "Amount_Log",
    "Currency_Match",
    "Same_Account",
    "Same_Bank",
    "Unknown_Bank_Involved",
]

MODEL_CATEGORICAL_FEATURES = [
    "Receiving Currency",
    "Payment Currency",
    "Payment Format",
    "Bank_Knowledge",
]

KNOWN_COUNTRY_NAMES = [
    "Australia", "Brazil", "Canada", "China", "France",
    "Germany", "India", "Israel", "Italy", "Japan",
    "Mexico", "Netherlands", "Portugal", "Russia",
    "Saudi Arabia", "Spain", "Switzerland", "UK",
    "Finland", "Greece", "Ireland", "Austria"
]

def is_bank_unknown(bank_id: int, bank_name: str = "") -> bool:
    """Check if bank ID or bank name belongs to unknown bank country category."""
    if not bank_name:
        return (bank_id % 3 == 0)
    bank_name_lower = str(bank_name).lower()
    return not any(country.lower() in bank_name_lower for country in KNOWN_COUNTRY_NAMES)

def build_raw_feature_df(raw_tx_dict: dict, account_stats: dict = None) -> pd.DataFrame:
    """
    Transforms raw transaction dictionary into a 43-column pandas DataFrame
    matching the exact feature list and column ordering used during training.
    """
    if account_stats is None:
        account_stats = {}

    df = pd.DataFrame([raw_tx_dict])

    ts = pd.to_datetime(df["Timestamp"].iloc[0])

    hour = int(ts.hour)
    day = int(ts.day)
    dow = int(ts.dayofweek)

    is_weekend = int(dow >= 5)
    is_night = int(hour < 6 or hour >= 22)

    amount_received = float(df["Amount Received"].iloc[0])
    amount_paid = float(df["Amount Paid"].iloc[0])

    amount_diff = amount_received - amount_paid
    amount_abs_diff = abs(amount_diff)
    amount_ratio = amount_received / (amount_paid if amount_paid != 0 else np.nan)
    if pd.isna(amount_ratio):
        amount_ratio = 1.0
    amount_log = float(np.log1p(max(0.0, amount_received)))

    currency_match = int(str(df["Receiving Currency"].iloc[0]).strip().lower() == str(df["Payment Currency"].iloc[0]).strip().lower())
    same_account = int(str(df["Account"].iloc[0]) == str(df["Account.1"].iloc[0]))
    same_bank = int(int(df["From Bank"].iloc[0]) == int(df["To Bank"].iloc[0]))

    from_bank = int(df["From Bank"].iloc[0])
    to_bank = int(df["To Bank"].iloc[0])

    from_unknown = is_bank_unknown(from_bank)
    to_unknown = is_bank_unknown(to_bank)

    if not from_unknown and not to_unknown:
        bank_knowledge = "Known_Known"
    elif from_unknown and not to_unknown:
        bank_knowledge = "Unknown_Known"
    elif not from_unknown and to_unknown:
        bank_knowledge = "Known_Unknown"
    else:
        bank_knowledge = "Unknown_Unknown"

    unknown_bank_involved = int(from_unknown or to_unknown)

    # Historical stats from account_stats dict or intelligent default estimation
    sender_key = f"{from_bank}_{df['Account'].iloc[0]}"
    receiver_key = f"{to_bank}_{df['Account.1'].iloc[0]}"
    rel_key = f"{sender_key}->{receiver_key}"

    sender_info = account_stats.get(sender_key, {})
    receiver_info = account_stats.get(receiver_key, {})
    rel_info = account_stats.get(rel_key, {})

    s_count = sender_info.get("Sender_Transaction_Count", 5)
    s_total = sender_info.get("Sender_Total_Amount", amount_paid * 4.5)
    s_max = sender_info.get("Sender_Max_Amount", max(amount_paid, amount_paid * 1.5))
    s_avg = s_total / s_count if s_count > 0 else amount_paid
    s_receivers = sender_info.get("Sender_Unique_Receivers", 2)
    s_days = sender_info.get("Sender_Unique_Days", 3)
    s_hours = sender_info.get("Sender_Active_Hours", 4)
    s_weekend = sender_info.get("Sender_Weekend_Transactions", is_weekend)
    s_night = sender_info.get("Sender_Night_Transactions", is_night)
    s_daily_avg = s_count / s_days if s_days > 0 else float(s_count)

    r_count = receiver_info.get("Receiver_Transaction_Count", 6)
    r_total = receiver_info.get("Receiver_Total_Amount", amount_received * 5.0)
    r_max = receiver_info.get("Receiver_Max_Amount", max(amount_received, amount_received * 1.8))
    r_avg = r_total / r_count if r_count > 0 else amount_received
    r_senders = receiver_info.get("Receiver_Unique_Senders", 3)
    r_days = receiver_info.get("Receiver_Unique_Days", 4)
    r_hours = receiver_info.get("Receiver_Active_Hours", 5)
    r_weekend = receiver_info.get("Receiver_Weekend_Transactions", is_weekend)
    r_night = receiver_info.get("Receiver_Night_Transactions", is_night)
    r_daily_avg = r_count / r_days if r_days > 0 else float(r_count)

    rel_count = rel_info.get("Relationship_Transaction_Count", 2)
    rel_total = rel_info.get("Relationship_Total_Amount", amount_received * 1.8)
    rel_max = rel_info.get("Relationship_Max_Amount", max(amount_received, amount_received * 1.2))
    rel_avg = rel_total / rel_count if rel_count > 0 else amount_received

    features = {
        "Amount Received": amount_received,
        "Amount Paid": amount_paid,
        "Sender_Transaction_Count": s_count,
        "Sender_Total_Amount": s_total,
        "Sender_Max_Amount": s_max,
        "Sender_Average_Amount": s_avg,
        "Sender_Unique_Receivers": s_receivers,
        "Sender_Unique_Days": s_days,
        "Sender_Active_Hours": s_hours,
        "Sender_Weekend_Transactions": s_weekend,
        "Sender_Night_Transactions": s_night,
        "Sender_Average_Daily_Transactions": s_daily_avg,
        "Receiver_Transaction_Count": r_count,
        "Receiver_Total_Amount": r_total,
        "Receiver_Max_Amount": r_max,
        "Receiver_Average_Amount": r_avg,
        "Receiver_Unique_Senders": r_senders,
        "Receiver_Unique_Days": r_days,
        "Receiver_Active_Hours": r_hours,
        "Receiver_Weekend_Transactions": r_weekend,
        "Receiver_Night_Transactions": r_night,
        "Receiver_Average_Daily_Transactions": r_daily_avg,
        "Relationship_Transaction_Count": rel_count,
        "Relationship_Total_Amount": rel_total,
        "Relationship_Max_Amount": rel_max,
        "Relationship_Average_Amount": rel_avg,
        "Hour": hour,
        "Day": day,
        "DayOfWeek": dow,
        "IsWeekend": is_weekend,
        "IsNight": is_night,
        "Amount_Difference": amount_diff,
        "Amount_Absolute_Difference": amount_abs_diff,
        "Amount_Ratio": amount_ratio,
        "Amount_Log": amount_log,
        "Currency_Match": currency_match,
        "Same_Account": same_account,
        "Same_Bank": same_bank,
        "Unknown_Bank_Involved": unknown_bank_involved,
        "Receiving Currency": str(df["Receiving Currency"].iloc[0]),
        "Payment Currency": str(df["Payment Currency"].iloc[0]),
        "Payment Format": str(df["Payment Format"].iloc[0]),
        "Bank_Knowledge": bank_knowledge,
    }

    feature_df = pd.DataFrame([features])
    ordered_cols = MODEL_NUMERIC_FEATURES + MODEL_CATEGORICAL_FEATURES
    return feature_df[ordered_cols]
