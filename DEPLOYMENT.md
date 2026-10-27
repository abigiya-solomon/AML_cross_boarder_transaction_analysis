# AML Cross-Border Transaction Analysis — Deployment Guide

This guide walks you through deploying the **Backend & ML Inference Service on Render** and the **Frontend Dashboard on Vercel**.

---

## 📁 Architecture Overview

```text
  [ Vercel: React + Vite + Tailwind ]
                  │
                  ▼ HTTPS REST Requests (VITE_API_URL)
  [ Render: FastAPI + LightGBM + SQLite/Postgres ]
                  │
      ┌───────────┴───────────┐
      ▼                       ▼
 [ ML Inference Engine ]   [ SQLite DB ]
 (ColumnTransformer +     (Transactions, Predictions,
  LightGBM Classifier)     Batch Upload Audits)
```

---

## Part 1: Push Project to GitHub

Before deploying, ensure your project is committed to a GitHub repository:

```bash
git init
git add .
git commit -m "feat: complete AML full-stack platform with deployment configs"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```

---

## Part 2: Deploy Backend & ML on Render

Render provides free and paid cloud hosting. Because LightGBM relies on OpenMP (`libgomp`), **Docker deployment** is the recommended method to guarantee binary compatibility.

### Method A: 1-Click Blueprint (Recommended)

1. Go to [Render Dashboard](https://dashboard.render.com).
2. Click **New +** $\rightarrow$ **Blueprint**.
3. Connect your GitHub repository.
4. Render will detect `render.yaml` at the root and pre-configure the service:
   - **Service Name**: `aml-cross-border-backend`
   - **Runtime**: `Docker`
   - **Health Check**: `/api/health`
5. Click **Apply**.
6. Wait for the build to complete. Once live, Render will assign your backend a public URL, for example:
   ```text
   https://aml-cross-border-backend.onrender.com
   ```

### Method B: Manual Web Service Setup (Docker)

If creating manually without Blueprint:
1. In Render, click **New +** $\rightarrow$ **Web Service**.
2. Select your repository.
3. Configure settings:
   - **Name**: `aml-cross-border-backend`
   - **Region**: Oregon or Ohio (or closest to you)
   - **Branch**: `main`
   - **Root Directory**: *(leave blank to use project root)*
   - **Runtime**: **Docker**
   - **Dockerfile Path**: `./Dockerfile`
   - **Instance Type**: **Free**
4. Under **Environment Variables**, add:
   - `PORT`: `10000`
   - `CORS_ORIGINS`: `*`
5. Under **Health Check Path**: `/api/health`
6. Click **Create Web Service**.

### Method C: Native Python Runtime (Alternative)

If you prefer Render's native Python runtime:
- **Runtime**: `Python`
- **Root Directory**: `backend`
- **Build Command**: `./build.sh`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Environment Variables**:
  - `PYTHON_VERSION`: `3.11.9`
  - `CORS_ORIGINS`: `*`

---

## Part 3: Deploy Frontend on Vercel

Vercel provides edge hosting optimized for React/Vite frontends.

1. Go to [Vercel Dashboard](https://vercel.com/dashboard).
2. Click **Add New...** $\rightarrow$ **Project**.
3. Select your GitHub repository and click **Import**.
4. Configure Project Settings:
   - **Project Name**: `aml-cross-border-dashboard`
   - **Framework Preset**: `Vite`
   - **Root Directory**: Click **Edit** and choose `frontend`.
5. Expand **Environment Variables**:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://<your-render-backend-name>.onrender.com/api`
   *(Be sure to include the `/api` prefix and your actual Render URL)*
6. Click **Deploy**.

> **Note on Client-Side Routing**: The included `frontend/vercel.json` already contains rewrite rules (`/(.*) -> /index.html`), ensuring browser refreshes on routes like `/transactions` or `/predict` will not trigger 404 errors.

---

## Part 4: Connect & Tighten Security (Post-Deployment)

1. Test the backend health endpoint in your browser:
   ```text
   https://<your-render-backend-name>.onrender.com/api/health
   ```
   You should see:
   ```json
   {
     "status": "healthy",
     "service": "AML Cross-Border Transaction Monitoring System",
     "version": "1.0.0",
     "model_loaded": true,
     "model_name": "LightGBM",
     "threshold": 0.5
   }
   ```
2. Open your Vercel deployment URL (e.g. `https://aml-cross-border-dashboard.vercel.app`).
3. In Render Dashboard $\rightarrow$ Web Service $\rightarrow$ **Environment**:
   Update `CORS_ORIGINS` to your exact Vercel domain:
   ```text
   https://aml-cross-border-dashboard.vercel.app,http://localhost:3000
   ```
   Click **Save Changes**.

---

## 🔍 Verification Checklist

- [x] Backend responds to `GET /api/health` with `status: healthy` and `model_loaded: true`.
- [x] Single prediction form (`/predict`) generates LightGBM probability and risk badges.
- [x] Batch CSV upload (`/upload`) accepts and scores transaction files.
- [x] Dashboard (`/`) renders KPI cards and time-series Recharts graphs.
- [x] Transaction Registry (`/transactions`) filters, searches, and paginates records.
- [x] Client-side routing refreshes cleanly on Vercel without 404 errors.
