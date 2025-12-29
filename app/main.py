"""
main.py

Application entry point for the GA4 Data API Connector service.

- Initializes the FastAPI application
- Registers API routers
- Exposes a basic health check endpoint

This file should remain lightweight and avoid business logic.
"""

from fastapi import FastAPI
from app.routes.ga4 import router as ga4_router

app = FastAPI(title="GA4 Data API Connector")

app.include_router(ga4_router)

@app.get("/health")
def health():
    """
    Health check endpoint used for readiness/liveness probes.
    """
    return {"status": "ok"}
