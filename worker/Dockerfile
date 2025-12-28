FROM python:3.11-slim

WORKDIR /app
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY backend /app/backend
COPY worker /app/worker
COPY corpus /app/corpus

ENV PYTHONPATH=/app
WORKDIR /app
