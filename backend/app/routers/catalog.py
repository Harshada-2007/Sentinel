import pandas as pd
from fastapi import APIRouter
from app.db import get_store
from app.services import stockout_service

router = APIRouter(prefix="/api", tags=["catalog"])


def _clean(df):
    return df.astype(object).where(pd.notnull(df), None).to_dict(orient="records")


@router.get("/products")
def products():
    return _clean(get_store().get_table("products"))


@router.get("/warehouses")
def warehouses():
    return _clean(get_store().get_table("warehouses"))


@router.get("/inventory-heatmap")
def inventory_heatmap():
    df = stockout_service.score_all()
    cols = ["product_id", "name", "warehouse_id", "quantity_on_hand", "days_of_cover", "stockout_probability"]
    out = df[cols].copy()
    out["days_of_cover"] = out["days_of_cover"].round(1)
    out["stockout_probability"] = out["stockout_probability"].round(3)
    return _clean(out)


@router.get("/audit")
def audit():
    df = get_store().get_table("audit_log")
    if df.empty:
        return []
    return _clean(df.iloc[::-1])
