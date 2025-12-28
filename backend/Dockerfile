FROM python:3.11-slim

WORKDIR /app
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY backend /app
COPY scripts /app/scripts

ENV PYTHONPATH=/app
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000
