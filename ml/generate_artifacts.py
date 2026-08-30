import os
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from lightgbm import LGBMClassifier

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

TARGET_COLUMN = "Is Laundering"

CURRENCIES = [
    "Australian Dollar", "Bitcoin", "Brazil Real", "Canadian Dollar",
    "Euro", "Mexican Peso", "Ruble", "Rupee", "Saudi Riyal",
    "Shekel", "Swiss Franc", "UK Pound", "US Dollar", "Yen", "Yuan"
]

PAYMENT_FORMATS = [
    "ACH", "Bitcoin", "Cash", "Cheque", "Credit Card", "Reinvestment", "Wire"
]

BANK_KNOWLEDGE_CATS = [
    "Known_Known", "Known_Unknown", "Unknown_Known", "Unknown_Unknown"
]

def generate_sample_data(n_samples=5000):
    np.random.seed(42)
    
    data = {}
    for col in MODEL_NUMERIC_FEATURES:
        if "Count" in col or "Days" in col or "Hours" in col or "Transactions" in col or "Senders" in col or "Receivers" in col:
            data[col] = np.random.randint(0, 50, size=n_samples)
        elif "Is" in col or "Match" in col or "Same" in col or "Involved" in col:
            data[col] = np.random.randint(0, 2, size=n_samples)
        elif "Hour" == col:
            data[col] = np.random.randint(0, 24, size=n_samples)
        elif "Day" == col:
            data[col] = np.random.randint(1, 29, size=n_samples)
        elif "DayOfWeek" == col:
            data[col] = np.random.randint(0, 7, size=n_samples)
        elif "Amount_Ratio" == col:
            data[col] = np.random.uniform(0.1, 2.0, size=n_samples)
        elif "Amount_Log" == col:
            data[col] = np.log1p(np.random.exponential(scale=5000, size=n_samples))
        elif "Difference" in col:
            data[col] = np.random.normal(0, 100, size=n_samples)
        else:
            data[col] = np.random.exponential(scale=5000, size=n_samples)
            
    data["Receiving Currency"] = np.random.choice(CURRENCIES, size=n_samples)
    data["Payment Currency"] = np.random.choice(CURRENCIES, size=n_samples)
    data["Payment Format"] = np.random.choice(PAYMENT_FORMATS, size=n_samples)
    data["Bank_Knowledge"] = np.random.choice(BANK_KNOWLEDGE_CATS, size=n_samples)
    
    prob = 0.05 + 0.3 * (data["Sender_Night_Transactions"] > 5) + 0.4 * (data["Amount Paid"] > 20000)
    prob = np.clip(prob, 0, 1)
    data[TARGET_COLUMN] = (np.random.uniform(0, 1, size=n_samples) < prob).astype(int)
    
    return pd.DataFrame(data)

def main():
    print("Generating sample training dataset...")
    df = generate_sample_data(10000)
    
    X_train = df[MODEL_NUMERIC_FEATURES + MODEL_CATEGORICAL_FEATURES].copy()
    y_train = df[TARGET_COLUMN].copy()
    
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "onehot",
                OneHotEncoder(
                    categories=[CURRENCIES, CURRENCIES, PAYMENT_FORMATS, BANK_KNOWLEDGE_CATS],
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
            ),
        ]
    )
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_transformer, MODEL_NUMERIC_FEATURES),
            ("categorical", categorical_transformer, MODEL_CATEGORICAL_FEATURES),
        ]
    )
    
    print("Fitting preprocessor...")
    X_train_processed = preprocessor.fit_transform(X_train)
    PROCESSED_FEATURE_NAMES = list(preprocessor.get_feature_names_out())
    
    X_train_df = pd.DataFrame(
        X_train_processed,
        columns=PROCESSED_FEATURE_NAMES,
        index=X_train.index
    )
    
    print(f"Processed feature count: {len(PROCESSED_FEATURE_NAMES)}")
    
    print("Fitting LightGBM classifier...")
    lgbm = LGBMClassifier(
        n_estimators=200,
        learning_rate=0.08,
        num_leaves=31,
        max_depth=-1,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=10,
        n_jobs=-1,
        random_state=42,
        verbosity=-1
    )
    lgbm.fit(X_train_df, y_train)
    
    artifacts_dir = os.path.join("ml", "artifacts")
    os.makedirs(artifacts_dir, exist_ok=True)
    
    model_path = os.path.join(artifacts_dir, "lightgbm_model.pkl")
    prep_path = os.path.join(artifacts_dir, "preprocessor.pkl")
    feats_path = os.path.join(artifacts_dir, "processed_feature_names.pkl")
    cfg_path = os.path.join(artifacts_dir, "model_config.pkl")
    
    joblib.dump(lgbm, model_path)
    joblib.dump(preprocessor, prep_path)
    joblib.dump(PROCESSED_FEATURE_NAMES, feats_path)
    
    model_config = {
        "model_name": "LightGBM",
        "threshold": 0.50,
        "number_of_features": len(PROCESSED_FEATURE_NAMES),
        "target_column": TARGET_COLUMN,
    }
    joblib.dump(model_config, cfg_path)
    
    print("Successfully generated all ML artifacts in:", artifacts_dir)

if __name__ == "__main__":
    main()
