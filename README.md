# 🛡️ AML Cross-Border Transaction Analysis & Monitoring Platform

[![Live Frontend](https://img.shields.io/badge/Vercel-Live%20Dashboard-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://aml-cross-boarder-transaction-analy-two.vercel.app)
[![Live Backend](https://img.shields.io/badge/Render-API%20Live-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://aml-cross-boarder-transaction-analysis.onrender.com/docs)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![LightGBM](https://img.shields.io/badge/Model-LightGBM-brightgreen?style=for-the-badge)](https://lightgbm.readthedocs.io)

An enterprise-grade, full-stack Anti-Money Laundering (AML) monitoring and inference platform designed to detect suspicious cross-border transactions in real time. Powered by an optimized **LightGBM** classifier with 43 behavioral features, strict anti-data-leakage temporal constraints, and composite account resolution.

---

## 🌐 Live Deployments

| Component | Platform | URL | Description |
| :--- | :--- | :--- | :--- |
| **Frontend UI** | **Vercel** | [aml-cross-boarder-transaction-analy-two.vercel.app](https://aml-cross-boarder-transaction-analy-two.vercel.app) | Interactive AML dashboard, registry, single prediction & CSV batch upload. |
| **Backend REST API** | **Render** | [aml-cross-boarder-transaction-analysis.onrender.com](https://aml-cross-boarder-transaction-analysis.onrender.com) | FastAPI ML inference service with Swagger UI at `/docs`. |
| **Health Check** | **Render** | [api/health](https://aml-cross-boarder-transaction-analysis.onrender.com/api/health) | Live service status & ML model readiness endpoint. |

---

## 🏛️ System Architecture

```text
 ┌────────────────────────────────────────────────────────┐
 │            Vercel Client (React 18 + Tailwind)         │
 │  Dashboard • Transaction Registry • Manual Inference   │
 └───────────────────────────┬────────────────────────────┘
                             │ HTTPS REST Requests
                             ▼
 ┌────────────────────────────────────────────────────────┐
 │           Render Server (FastAPI + Uvicorn)            │
 │  Route Handlers • Pydantic V2 • SQLite / PostgreSQL    │
 └─────────────┬─────────────────────────────┬────────────┘
               ▼                             ▼
 ┌───────────────────────────┐ ┌───────────────────────────┐
 │   Feature Engine (43 cols)│ │     Database Registry     │
 │  Sender, Receiver, Bank   │ │ Transactions, Predictions,│
 │  & Relationship Features  │ │ Audit Upload Records      │
 └─────────────┬─────────────┘ └───────────────────────────┘
               ▼
 ┌───────────────────────────┐
 │ Preprocessor (80 features)│
 │ SimpleImputer + OneHotEnc │
 └─────────────┬─────────────┘
               ▼
 ┌───────────────────────────┐
 │   LightGBM Classifier     │ ──► Suspicious Probability ──► Risk Level:
 │   (Threshold = 0.50)      │                                LOW / MEDIUM / HIGH / CRITICAL
 └───────────────────────────┘
```

---

## 📊 Model Performance & Benchmarks

The LightGBM model was selected after 5-fold chronological cross-validation across 7 candidate algorithms (Logistic Regression, Random Forest, Extra Trees, HistGradientBoosting, XGBoost, LightGBM, and CatBoost).

| Metric | Score | Description |
| :--- | :--- | :--- |
| **Precision** | **91.67%** | Correctly identified laundering when flagging suspicious activity |
| **Recall** | **99.87%** | Detected 781 out of 782 total laundering cases (missing only 1) |
| **F1 Score** | **95.59%** | Harmonic mean balancing false alerts with missed laundering |
| **ROC-AUC** | **96.59%** | High discriminative power across threshold spectrum |
| **PR-AUC** | **96.73%** | Superior ranking ability for rare positive class |
| **Decision Threshold** | **0.50** | Enforced fixed classification boundary |

### Test Confusion Matrix
* **True Negatives (TN)**: 473
* **False Positives (FP)**: 71
* **False Negatives (FN)**: 1
* **True Positives (TP)**: 781

---

## 🚀 Key Features

1. **AML Monitoring Dashboard**:
   - Real-time KPIs: Total Transactions, Suspicious Ratio, High-Risk Volume, Average Risk Score.
   - Temporal Area Charts: Tracking suspicious events and total transaction flow over time.
   - Categorical Insights: Payment format distribution, currency breakdown, and risk severity pie chart.

2. **Transaction Registry**:
   - Full filtering by Risk Level (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`), Payment Format, Currency, or Suspicious-only status.
   - Search across composite accounts and Bank IDs with pagination and column sorting.
   - Modal deep-dive viewing raw attributes and all 43 computed model features.

3. **Single Transaction Inference**:
   - Interactive manual form for investigator ad-hoc risk evaluation.
   - Real-time probability gauge, risk classification badge, and breakdown of derived behavioral metrics.

4. **Batch CSV Upload & Audit**:
   - Drag-and-drop CSV batch upload supporting standard IBM AML transaction formats.
   - Streaming row-by-row validation, batch inference, and automated summary statistics.

5. **Model Performance Auditor**:
   - In-dashboard inspection of benchmark models, validation curves, and confusion matrix data.

6. **Anti-Data-Leakage Safeguards**:
   - Strict chronological dataset partitioning (Train: Sept 1–16, Val: Sept 17–20, Test: Sept 21–28).
   - Composite account identity enforcement (`Bank ID + Account`).

---

## 🔌 API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Service health status and ML model loaded flag |
| `POST` | `/api/predict` | Run instant risk inference for a single raw transaction |
| `POST` | `/api/predict/upload` | Process batch CSV transaction dataset |
| `GET` | `/api/transactions` | Query paginated transaction registry with filters and search |
| `GET` | `/api/transactions/{id}` | Retrieve transaction investigation details & feature breakdown |
| `GET` | `/api/dashboard/stats` | Aggregated KPI metrics, time-series, and distribution charts |
| `GET` | `/api/model/info` | Test performance metrics and benchmark comparison |

Interactive Swagger documentation is available at:  
👉 **`https://aml-cross-boarder-transaction-analysis.onrender.com/docs`**

---

## 💻 Local Development Setup

### Prerequisites
* Python 3.11+
* Node.js 18+ and npm

### 1. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run database setup & start server
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
API will run on `http://127.0.0.1:8000` (Docs: `http://127.0.0.1:8000/docs`).

### 2. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install packages
npm install

# Start Vite dev server
npm run dev
```
Dashboard will run on `http://localhost:3000` (auto-proxies `/api` calls to backend on port 8000).

### 3. Run Automated Tests
```bash
cd backend
python -m pytest tests
```

---

## 📦 Deployment

Full deployment instructions are available in [**DEPLOYMENT.md**](./DEPLOYMENT.md).

* **Render Deployment**: Uses the root [`Dockerfile`](./Dockerfile) and [`render.yaml`](./render.yaml) blueprint.
* **Vercel Deployment**: Configured via [`frontend/vercel.json`](./frontend/vercel.json) with client-side SPA routing and automated API proxying.

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
