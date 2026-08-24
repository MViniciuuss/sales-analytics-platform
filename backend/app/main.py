from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routes.auth import router as auth_router
from backend.app.routes.data import router as data_router
from backend.app.services.dashboard_service import (
    get_dashboard_charts,
    get_dashboard_summary,
)

app = FastAPI(
    title="Sales Analytics API",
    description="API da plataforma full stack de análise de vendas.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data_router)
app.include_router(auth_router)


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

@app.get("/api/dashboard/charts")
def dashboard_charts():
    return get_dashboard_charts()