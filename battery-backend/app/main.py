"""
Main FastAPI application - the shared entrypoint for the whole team.

Member B: add your router in app/routers/predictions.py and app/routers/copilot.py,
          then include_router() them below, same pattern as vehicles_router.
Member C: same idea - app/routers/simulation.py and app/routers/business_impact.py.

Run locally:
    uvicorn app.main:app --reload --port 8000

Then visit http://localhost:8000/docs for interactive Swagger docs -
useful for testing endpoints without needing the frontend running yet.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers.vehicles import router as vehicles_router

app = FastAPI(
    title="Battery Digital Twin Intelligence Platform API",
    description="EV Fleet Battery Health, Prediction, Simulation & Business Impact API",
    version="1.0.0",
)

# CORS - open for all origins during the hackathon so the Next.js frontend
# (running on a different port/domain) can call this API without issues.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.ALLOWED_ORIGINS == "*" else settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Register routers ---
app.include_router(vehicles_router)
# app.include_router(predictions_router)   <- Member B adds this
# app.include_router(copilot_router)       <- Member B adds this
# app.include_router(simulation_router)    <- Member C adds this
# app.include_router(business_impact_router)  <- Member C adds this


@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok"}


@app.get("/", tags=["system"])
def root():
    return {
        "message": "Battery Digital Twin API is running",
        "docs": "/docs",
    }
