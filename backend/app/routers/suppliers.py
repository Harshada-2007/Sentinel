import pandas as pd
from fastapi import APIRouter, HTTPException
from app.services import risk_service

router = APIRouter(prefix="/api/suppliers", tags=["suppliers"])


@router.get("")
def list_suppliers():
    df = risk_service.score_all_suppliers()
    cols = ["supplier_id", "name", "tier", "location", "lead_time_days", "unit_cost",
            "capacity_units", "reliability_score", "backup_for", "risk_score", "risk_tier"]
    df = df[cols].astype(object).where(pd.notnull(df[cols]), None)
    return df.to_dict(orient="records")


@router.get("/{supplier_id}/risk")
def supplier_risk(supplier_id: str):
    result = risk_service.get_supplier_risk(supplier_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return result
