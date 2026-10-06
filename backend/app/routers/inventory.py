from fastapi import APIRouter
from app.db import get_store
from app.services import stockout_service

router = APIRouter(prefix="/api/inventory", tags=["inventory"])


@router.get("")
def list_inventory():
    store = get_store()
    return store.get_table("inventory").to_dict(orient="records")


@router.get("/{product_id}/stockout-risk")
def stockout_risk(product_id: str):
    return stockout_service.get_stockout_risk(product_id)
