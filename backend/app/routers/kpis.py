from fastapi import APIRouter
from app.db import get_store
from app.services import risk_service, stockout_service

router = APIRouter(prefix="/api", tags=["kpis"])


@router.get("/kpis")
def get_kpis():
    store = get_store()
    events = store.get_table("disruption_events")
    orders = store.get_table("orders")
    products = store.get_table("products")

    risk_df = risk_service.score_all_suppliers()
    suppliers_at_risk = int((risk_df["risk_tier"] == "critical").sum())

    stockout_df = stockout_service.score_all()
    stockouts_predicted = int((stockout_df["stockout_probability"] >= 0.5).sum())

    open_orders = orders[~orders.status.isin(["delivered", "cancelled"])].merge(
        products[["product_id", "unit_price"]], on="product_id", how="left")
    open_orders["value"] = open_orders["quantity"] * open_orders["unit_price"]

    # exposure = value of open orders tied to at-risk suppliers' products
    at_risk_supplier_ids = risk_df[risk_df.risk_tier.isin(["critical", "warning"])]["supplier_id"].tolist()
    at_risk_products = products[products.supplier_id.isin(at_risk_supplier_ids)]["product_id"].tolist()
    exposure = float(open_orders[open_orders.product_id.isin(at_risk_products)]["value"].sum())

    active_events = int(len(events))

    return {
        "suppliers_at_risk": suppliers_at_risk,
        "dollar_exposure": round(exposure, 2),
        "stockouts_predicted": stockouts_predicted,
        "active_events": active_events,
    }
