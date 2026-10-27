import pandas as pd
import numpy as np

# 39 Numeric Features exactly matching notebook order
MODEL_NUMERIC_FEATURES = [
    # Sender features (10)
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
    # Receiver features (10)
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
    # Relationship features (4)
    "Relationship_Transaction_Count",
    "Relationship_Total_Amount",
    "Relationship_Max_Amount",
    "Relationship_Average_Amount",
    # Bank knowledge features (1 numeric)
    "Unknown_Unknown_Transfer",
    # Transaction-level features (14 numeric)
    "Amount Received",
    "Amount Paid",
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
]

# 4 Categorical Features
MODEL_CATEGORICAL_FEATURES = [
    "Receiving Currency",
    "Payment Currency",
    "Payment Format",
    "Bank_Knowledge",
]

# Known banks set from notebook
UNKNOWN_BANK_IDS = {20, 114, 189, 219, 238, 287, 303, 3196, 3215, 3314}

def create_composite_account_key(bank_id: int, account_num: str) -> str:
    """Composite account key: Bank ID + Account Number."""
    return f"{bank_id}_{account_num}"

def add_transaction_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    df["Hour"] = df["Timestamp"].dt.hour.astype("int8")
    df["Day"] = df["Timestamp"].dt.day.astype("int8")
    df["DayOfWeek"] = df["Timestamp"].dt.dayofweek.astype("int8")
    df["IsWeekend"] = (df["DayOfWeek"] >= 5).astype("int8")
    df["IsNight"] = ((df["Hour"] < 6) | (df["Hour"] >= 22)).astype("int8")

    df["Amount_Difference"] = df["Amount Received"] - df["Amount Paid"]
    df["Amount_Absolute_Difference"] = df["Amount_Difference"].abs()
    df["Amount_Ratio"] = df["Amount Received"] / df["Amount Paid"].replace(0, np.nan)
    df["Amount_Log"] = np.log1p(df["Amount Received"].clip(lower=0))

    df["Currency_Match"] = (df["Receiving Currency"] == df["Payment Currency"]).astype("int8")
    df["Same_Account"] = (df["Account"].astype(str) == df["Account.1"].astype(str)).astype("int8")
    df["Same_Bank"] = (df["From Bank"] == df["To Bank"]).astype("int8")

    return df

def add_bank_knowledge_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    from_unknown = df["From Bank"].isin(UNKNOWN_BANK_IDS)
    to_unknown = df["To Bank"].isin(UNKNOWN_BANK_IDS)

    bank_knowledge = pd.Series("Known -> Known", index=df.index)
    bank_knowledge[from_unknown & ~to_unknown] = "Unknown -> Known"
    bank_knowledge[~from_unknown & to_unknown] = "Known -> Unknown"
    bank_knowledge[from_unknown & to_unknown] = "Unknown -> Unknown"

    df["Bank_Knowledge"] = bank_knowledge
    df["Unknown_Unknown_Transfer"] = (df["Bank_Knowledge"] == "Unknown -> Unknown").astype("int8")
    return df

def build_feature_dataframe(transaction_data: dict, history_stats: dict = None) -> pd.DataFrame:
    """Transforms raw transaction dictionary into a single-row DataFrame ready for ColumnTransformer."""
    row = {
        "Timestamp": transaction_data.get("timestamp") or pd.Timestamp.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "From Bank": int(transaction_data["from_bank"]),
        "Account": str(transaction_data["account"]),
        "To Bank": int(transaction_data["to_bank"]),
        "Account.1": str(transaction_data["receiver_account"]),
        "Amount Received": float(transaction_data["amount_received"]),
        "Receiving Currency": str(transaction_data["receiving_currency"]),
        "Amount Paid": float(transaction_data["amount_paid"]),
        "Payment Currency": str(transaction_data["payment_currency"]),
        "Payment Format": str(transaction_data["payment_format"]),
    }
    
    df = pd.DataFrame([row])
    df = add_transaction_features(df)
    df = add_bank_knowledge_features(df)
    
    # Historical behavioral defaults or provided aggregations
    h = history_stats or {}
    amt_paid = df["Amount Paid"].iloc[0]
    amt_rcvd = df["Amount Received"].iloc[0]

    # Sender defaults
    df["Sender_Transaction_Count"] = h.get("Sender_Transaction_Count", 1.0)
    df["Sender_Total_Amount"] = h.get("Sender_Total_Amount", amt_paid)
    df["Sender_Max_Amount"] = h.get("Sender_Max_Amount", amt_paid)
    df["Sender_Average_Amount"] = h.get("Sender_Average_Amount", amt_paid)
    df["Sender_Unique_Receivers"] = h.get("Sender_Unique_Receivers", 1.0)
    df["Sender_Unique_Days"] = h.get("Sender_Unique_Days", 1.0)
    df["Sender_Active_Hours"] = h.get("Sender_Active_Hours", 1.0)
    df["Sender_Weekend_Transactions"] = h.get("Sender_Weekend_Transactions", float(df["IsWeekend"].iloc[0]))
    df["Sender_Night_Transactions"] = h.get("Sender_Night_Transactions", float(df["IsNight"].iloc[0]))
    df["Sender_Average_Daily_Transactions"] = h.get("Sender_Average_Daily_Transactions", 1.0)

    # Receiver defaults
    df["Receiver_Transaction_Count"] = h.get("Receiver_Transaction_Count", 1.0)
    df["Receiver_Total_Amount"] = h.get("Receiver_Total_Amount", amt_rcvd)
    df["Receiver_Max_Amount"] = h.get("Receiver_Max_Amount", amt_rcvd)
    df["Receiver_Average_Amount"] = h.get("Receiver_Average_Amount", amt_rcvd)
    df["Receiver_Unique_Senders"] = h.get("Receiver_Unique_Senders", 1.0)
    df["Receiver_Unique_Days"] = h.get("Receiver_Unique_Days", 1.0)
    df["Receiver_Active_Hours"] = h.get("Receiver_Active_Hours", 1.0)
    df["Receiver_Weekend_Transactions"] = h.get("Receiver_Weekend_Transactions", float(df["IsWeekend"].iloc[0]))
    df["Receiver_Night_Transactions"] = h.get("Receiver_Night_Transactions", float(df["IsNight"].iloc[0]))
    df["Receiver_Average_Daily_Transactions"] = h.get("Receiver_Average_Daily_Transactions", 1.0)

    # Relationship defaults
    df["Relationship_Transaction_Count"] = h.get("Relationship_Transaction_Count", 1.0)
    df["Relationship_Total_Amount"] = h.get("Relationship_Total_Amount", amt_paid)
    df["Relationship_Max_Amount"] = h.get("Relationship_Max_Amount", amt_paid)
    df["Relationship_Average_Amount"] = h.get("Relationship_Average_Amount", amt_paid)

    # Enforce exact ordering of 43 features
    feature_cols = MODEL_NUMERIC_FEATURES + MODEL_CATEGORICAL_FEATURES
    return df[feature_cols]
