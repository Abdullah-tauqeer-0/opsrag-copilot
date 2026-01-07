from prometheus_client import Counter, Histogram, generate_latest
from fastapi import Response

REQUESTS = Counter("opsrag_requests_total", "Total requests", ["endpoint"])
LATENCY = Histogram("opsrag_request_latency_seconds", "Request latency", ["endpoint"])


def setup_metrics(app):
    @app.middleware("http")
    async def metrics_middleware(request, call_next):
        endpoint = request.url.path
        with LATENCY.labels(endpoint).time():
            response = await call_next(request)
        REQUESTS.labels(endpoint).inc()
        return response

    @app.get("/metrics")
    def metrics():
        return Response(generate_latest(), media_type="text/plain")
