from fastapi import FastAPI

from backend.app.services.dashboard_service import (
    get_dashboard_summary,
)

app = FastAPI(
    title="Sales Analytics API",
    description="API da plataforma full stack de análise de vendas.",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Sales Analytics API",
        "status": "online",
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "sales-analytics-api",
    }

@app.get("/api/dashboard")
def dashboard():
    return get_dashboard_summary()