FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (libgomp1 required by LightGBM OpenMP)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY ml /app/ml
COPY backend /app/backend

# Generate ML artifacts inside container
WORKDIR /app/backend
RUN python /app/ml/generate_artifacts.py

ENV PORT=10000
ENV PYTHONPATH=/app/backend
ENV ML_ARTIFACTS_DIR=/app/ml/artifacts
EXPOSE 10000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}"]
