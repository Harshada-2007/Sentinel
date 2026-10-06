from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    suppliers, inventory, orders, events, predictions,
    impact, simulator, optimizer, explanations, kpis, catalog,
)

app = FastAPI(
    title="Sentinel Control Tower API",
    description="AI-powered supply chain risk prediction, impact analysis, and response optimization.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(suppliers.router)
app.include_router(inventory.router)
app.include_router(orders.router)
app.include_router(events.router)
app.include_router(predictions.router)
app.include_router(impact.router)
app.include_router(simulator.router)
app.include_router(optimizer.router)
app.include_router(explanations.router)
app.include_router(kpis.router)
app.include_router(catalog.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "Sentinel Control Tower API"}


@app.get("/health")
def health():
    return {"status": "healthy"}
