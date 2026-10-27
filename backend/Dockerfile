FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (libgomp1 required by LightGBM OpenMP)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . /app/backend
COPY ../ml /app/ml 2>/dev/null || :

# Generate ML artifacts if ml folder is copied, otherwise rely on backend/ml
WORKDIR /app/backend
RUN python -c "from app.ml.feature_engineering import *; print('Verifying imports...')"

ENV PORT=10000
ENV PYTHONPATH=/app/backend
EXPOSE 10000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}"]
