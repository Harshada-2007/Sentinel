from typing import Optional
from fastapi import APIRouter, Query
from app.db import get_store

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.get("")
def list_orders(customer_tier: Optional[str] = Query(None), warehouse_id: Optional[str] = Query(None),
                status: Optional[str] = Query(None), limit: int = Query(500, le=5000)):
    store = get_store()
    df = store.get_table("orders")
    if customer_tier:
        df = df[df.customer_tier == customer_tier]
    if warehouse_id:
        df = df[df.warehouse_id == warehouse_id]
    if status:
        df = df[df.status == status]
    return df.head(limit).to_dict(orient="records")
