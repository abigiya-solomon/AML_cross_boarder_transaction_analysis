# AML Cross-Border Transaction Analysis System — Full-Stack Platform

A production-style full-stack web platform for Anti-Money Laundering (AML) cross-border transaction analysis and risk prediction, powered by a trained **LightGBM** classifier.

---

## 🌟 Key Features

1. **AML Transaction Monitoring Dashboard**: Real-time KPI metrics, suspicious rate tracking, temporal risk trends, payment format distribution, currency breakdown, and top suspicious accounts/banks.
2. **Transaction Registry**: Search, paginate, and filter transactions by risk level, payment format, currency, or suspicious status.
3. **Single Transaction Inference**: Manual single transaction input form with instant probability score, risk level badge (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`), and complete 43-feature breakdown.
4. **Batch CSV Upload**: Drag-and-drop CSV upload for bulk inference with stream parsing, row validation, and real-time processing summary.
5. **Model Performance Auditor**: Display of notebook evaluation metrics (Precision: 91.67%, Recall: 99.87%, F1: 95.59%, ROC-AUC: 96.59%, PR-AUC: 96.73%, Threshold: 0.50) and test confusion matrix (TN: 473, FP: 71, FN: 1, TP: 781).
6. **Anti-Data-Leakage Safeguards**: Strict temporal separation enforcement and composite account identity resolution (`Bank ID + Account`).

---

## 🏗️ Architecture

```text
[ React 18 + Tailwind CSS + Recharts ]
                 │
                 ▼ (REST API)
[ FastAPI Backend (Python) ]
                 │
       ┌─────────┴─────────┐
       ▼                   ▼
[ Feature Engine ]  [ SQLite Database ]
       │            (Transactions, Predictions, Uploads)
       ▼
[ ColumnTransformer (.pkl) ]
       │
       ▼
[ LightGBM Classifier (.pkl) ] ──► Probability ──► Threshold 0.50 ──► Risk Classification
```

---

## 🚀 Quick Start Guide

### 1. Backend Setup

```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

* Backend API Docs: `http://127.0.0.1:8000/docs`
* Health Check: `http://127.0.0.1:8000/api/health`

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

* Dashboard UI: `http://localhost:3000`

---

## 🧪 Testing

Run backend unit tests:

```bash
$env:PYTHONPATH="backend"; python -m pytest backend/tests
```

---

## 📄 Saved ML Artifacts

Located in `ml/artifacts/`:
- `lightgbm_model.pkl`: Trained LightGBM model.
- `preprocessor.pkl`: Fitted `ColumnTransformer` (SimpleImputer + StandardScaler + OneHotEncoder).
- `processed_feature_names.pkl`: Exact 80 one-hot feature names.
- `model_config.pkl`: Threshold (0.50) and model metadata configuration.
