import pandas as pd

from app.db import get_store


def compute_impact(event_id: str) -> dict:
    store = get_store()
    events = store.get_table("disruption_events")
    suppliers = store.get_table("suppliers")
    products = store.get_table("products")
    orders = store.get_table("orders")

    event_row = events[events.event_id == event_id]
    if event_row.empty:
        return None
    event = event_row.iloc[0]

    supplier_row = suppliers[suppliers.supplier_id == event.affected_supplier_id]
    supplier = supplier_row.iloc[0] if not supplier_row.empty else None

    affected_products = products[products.supplier_id == event.affected_supplier_id]
    affected_product_ids = set(affected_products.product_id.tolist())

    # orders not yet delivered/cancelled for the affected products
    open_orders = orders[
        orders.product_id.isin(affected_product_ids)
        & ~orders.status.isin(["delivered", "cancelled"])
    ].merge(affected_products[["product_id", "unit_price", "name"]], on="product_id", how="left")

    open_orders["order_value"] = open_orders["quantity"] * open_orders["unit_price"]
    revenue_at_risk = float(open_orders["order_value"].sum())

    product_summaries = []
    for _, p in affected_products.iterrows():
        p_orders = open_orders[open_orders.product_id == p.product_id]
        product_summaries.append({
            "product_id": p.product_id,
            "name": p["name"],
            "orders_affected": int(len(p_orders)),
            "value_at_risk": round(float(p_orders["order_value"].sum()), 2),
        })
    product_summaries.sort(key=lambda x: -x["value_at_risk"])

    warehouses_affected = open_orders["warehouse_id"].dropna().unique().tolist() if not open_orders.empty else []

    cascade = {
        "event": {"event_id": event.event_id, "event_type": event.event_type,
                  "severity": float(event.severity), "predicted_delay_days": int(event.predicted_delay_days)},
        "supplier": {"supplier_id": supplier.supplier_id, "name": supplier["name"],
                     "location": supplier.location} if supplier is not None else None,
        "products": [p["product_id"] for p in product_summaries],
        "warehouses": warehouses_affected,
        "orders_count": int(len(open_orders)),
    }

    return {
        "event_id": event_id,
        "affected_supplier": {
            "supplier_id": supplier.supplier_id, "name": supplier["name"],
            "location": supplier.location, "reliability_score": float(supplier.reliability_score),
        } if supplier is not None else {},
        "affected_products": product_summaries,
        "affected_orders_count": int(len(open_orders)),
        "revenue_at_risk": round(revenue_at_risk, 2),
        "cascade": cascade,
    }
