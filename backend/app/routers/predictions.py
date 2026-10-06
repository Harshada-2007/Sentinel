from fastapi import APIRouter, HTTPException
from app.services import demand_service, risk_service

router = APIRouter(prefix="/api/predictions", tags=["predictions"])


@router.get("/demand/{product_id}")
def demand_forecast(product_id: str):
    forecast = demand_service.forecast_product(product_id)
    if not forecast:
        raise HTTPException(status_code=404, detail="No demand history for product")
    return {"product_id": product_id, "forecast": forecast}


@router.get("/suppliers")
def ranked_suppliers():
    df = risk_service.score_all_suppliers()
    df = df.sort_values("risk_score", ascending=False)
    cols = ["supplier_id", "name", "tier", "location", "risk_score", "risk_tier"]
    return df[cols].to_dict(orient="records")
