# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (optional; keep slim)
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY services ./services

# Runtime env (can be overridden at deploy time)
ENV MONGODB_URI="mongodb://mongodb:27017" \
    DB_NAME="enemy_soldiers" \
    COLLECTION_NAME="soldier_details"

EXPOSE 8000

CMD ["uvicorn", "services.data_loader.api:app", "--host", "0.0.0.0", "--port", "8000"]