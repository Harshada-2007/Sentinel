"""
levers.py — The 5 response levers. Each evaluate(...) call is grounded in
real rows pulled from the data store (suppliers, products, inventory,
orders) for the given disruption event, and returns:
    {cost, stockout_reduction, sla_impact, feasibility, description}

`units` is the quantity of affected demand the lever is asked to cover
(0.0-1.0 fraction of total shortfall, scaled by `qty_fraction` param).
"""
from app.db import get_store
from app.services.impact_service import compute_impact

USD_TO_INR = 83.0
TRANSFER_COST_PER_UNIT = 6.5 * USD_TO_INR  # INR per unit moved between warehouses
REORDER_PENALTY_PER_UNIT_DAY = 0.05 * USD_TO_INR
DEPRIORITIZE_PENALTY_PER_ORDER = 150.0 * USD_TO_INR
PROMO_MARGIN_LOSS_RATE = 0.15    # fraction of unit price lost per unit of demand shed


def _shortfall_units(event_id: str) -> int:
    """Total quantity across all open orders tied to the disrupted supplier."""
    store = get_store()
    orders = store.get_table("orders")
    products = store.get_table("products")
    impact = compute_impact(event_id)
    if not impact:
        return 0
    pids = [p["product_id"] for p in impact["affected_products"]]
    open_orders = orders[orders.product_id.isin(pids) & ~orders.status.isin(["delivered", "cancelled"])]
    return int(open_orders["quantity"].sum())


def lever_1_switch_supplier(event_id: str, params: dict) -> dict:
    """Switch to backup supplier — cost = (backup_unit_cost - primary_unit_cost) x qty."""
    store = get_store()
    suppliers = store.get_table("suppliers")
    events = store.get_table("disruption_events")
    event = events[events.event_id == event_id].iloc[0]
    primary = suppliers[suppliers.supplier_id == event.affected_supplier_id]
    if primary.empty:
        return {"lever": 1, "cost": 0, "stockout_reduction": 0, "sla_impact": 0,
                "feasibility": 0, "description": "No primary supplier found."}
    primary = primary.iloc[0]
    backups = suppliers[suppliers.backup_for == primary.supplier_id].sort_values("reliability_score", ascending=False)
    total_units = _shortfall_units(event_id)
    frac = float(params.get("qty_fraction", 0.6))
    qty = total_units * frac

    if backups.empty or qty <= 0:
        return {"lever": 1, "cost": 0, "stockout_reduction": 0, "sla_impact": 0,
                "feasibility": 0, "description": "No qualified backup supplier available."}
    backup = backups.iloc[0]
    qty = min(qty, backup.capacity_units)
    cost = max(0.0, (backup.unit_cost - primary.unit_cost)) * qty
    stockout_reduction = min(0.9, 0.75 * frac * backup.reliability_score)
    sla_impact = 0.02 * frac  # small positive SLA gain from added supply
    return {
        "lever": 1, "cost": round(float(cost), 2),
        "stockout_reduction": round(float(stockout_reduction), 3),
        "sla_impact": round(float(sla_impact), 3), "feasibility": 1.0,
        "description": f"Switch {int(qty)} units to backup supplier {backup['name']} "
                        f"(+₹{backup.unit_cost - primary.unit_cost:.2f}/unit, lead time {int(backup.lead_time_days)}d).",
    }


def lever_2_transfer_inventory(event_id: str, params: dict) -> dict:
    """Transfer inventory between warehouses — cost = transfer_cost_per_unit x qty."""
    store = get_store()
    inventory = store.get_table("inventory")
    impact = compute_impact(event_id)
    pids = [p["product_id"] for p in impact["affected_products"]] if impact else []
    total_units = _shortfall_units(event_id)
    frac = float(params.get("qty_fraction", 0.4))
    needed = total_units * frac

    surplus = inventory[inventory.product_id.isin(pids)].copy()
    surplus_units = float(surplus["quantity_on_hand"].sum() * 0.3)  # assume ~30% is transferable surplus
    qty = min(needed, surplus_units)
    if qty <= 0:
        return {"lever": 2, "cost": 0, "stockout_reduction": 0, "sla_impact": 0,
                "feasibility": 0, "description": "No transferable surplus inventory found."}
    cost = TRANSFER_COST_PER_UNIT * qty
    stockout_reduction = min(0.8, 0.5 * (qty / total_units if total_units else 0))
    sla_impact = 0.03 * (qty / total_units if total_units else 0)
    return {
        "lever": 2, "cost": round(float(cost), 2),
        "stockout_reduction": round(float(stockout_reduction), 3),
        "sla_impact": round(float(sla_impact), 3), "feasibility": 1.0,
        "description": f"Transfer {int(qty)} units of surplus inventory between warehouses "
                        f"(₹{TRANSFER_COST_PER_UNIT:.2f}/unit, arrives in ~2 days).",
    }


def lever_3_reorder_timing(event_id: str, params: dict) -> dict:
    """Change reorder timing/quantity — cost = holding_cost x extra_units x days."""
    store = get_store()
    warehouses = store.get_table("warehouses")
    avg_holding = float(warehouses["holding_cost_per_unit_day"].mean()) if not warehouses.empty else 0.03
    total_units = _shortfall_units(event_id)
    frac = float(params.get("qty_fraction", 0.3))
    extra_units = total_units * frac
    days = int(params.get("extra_days", 10))
    cost = avg_holding * extra_units * days
    stockout_reduction = min(0.55, 0.4 * frac)
    sla_impact = 0.01 * frac
    return {
        "lever": 3, "cost": round(float(cost), 2),
        "stockout_reduction": round(float(stockout_reduction), 3),
        "sla_impact": round(float(sla_impact), 3), "feasibility": 1.0,
        "description": f"Expedite reorder of {int(extra_units)} extra units, held {days} days "
                        f"(₹{avg_holding:.3f}/unit/day).",
    }


def lever_4_prioritize_orders(event_id: str, params: dict) -> dict:
    """Prioritize critical (Tier-A) orders — cost = penalty x deprioritized_orders."""
    store = get_store()
    orders = store.get_table("orders")
    impact = compute_impact(event_id)
    pids = [p["product_id"] for p in impact["affected_products"]] if impact else []
    open_orders = orders[orders.product_id.isin(pids) & ~orders.status.isin(["delivered", "cancelled"])]
    tier_c_b = open_orders[open_orders.customer_tier.isin(["B", "C"])]
    deprioritized = int(len(tier_c_b) * float(params.get("deprioritize_fraction", 0.5)))
    cost = DEPRIORITIZE_PENALTY_PER_ORDER * deprioritized
    tier_a_count = int((open_orders.customer_tier == "A").sum())
    sla_impact = 0.06 if tier_a_count > 0 else 0.0
    stockout_reduction = 0.15  # doesn't reduce stockouts, but protects SLA for top-tier customers
    return {
        "lever": 4, "cost": round(float(cost), 2),
        "stockout_reduction": round(float(stockout_reduction), 3),
        "sla_impact": round(float(sla_impact), 3), "feasibility": 1.0,
        "description": f"Deprioritize {deprioritized} Tier-B/C orders to protect {tier_a_count} "
                        f"Tier-A commitments (₹{DEPRIORITIZE_PENALTY_PER_ORDER:.0f}/order penalty).",
    }


def lever_5_pricing_promo(event_id: str, params: dict) -> dict:
    """Adjust pricing/promotion — cost = margin_loss x demand_reduction."""
    store = get_store()
    products = store.get_table("products")
    impact = compute_impact(event_id)
    pids = [p["product_id"] for p in impact["affected_products"]] if impact else []
    total_units = _shortfall_units(event_id)
    frac = float(params.get("demand_reduction_fraction", 0.2))
    demand_reduction = total_units * frac
    avg_price = float(products[products.product_id.isin(pids)]["unit_price"].mean()) if pids else 0
    cost = PROMO_MARGIN_LOSS_RATE * avg_price * demand_reduction
    stockout_reduction = min(0.45, 0.6 * frac)
    sla_impact = 0.0
    return {
        "lever": 5, "cost": round(float(cost), 2),
        "stockout_reduction": round(float(stockout_reduction), 3),
        "sla_impact": round(float(sla_impact), 3), "feasibility": 1.0,
        "description": f"Reduce demand by {int(demand_reduction)} units via pricing/promotion "
                        f"({PROMO_MARGIN_LOSS_RATE*100:.0f}% margin loss rate).",
    }


LEVER_FUNCS = {
    1: lever_1_switch_supplier,
    2: lever_2_transfer_inventory,
    3: lever_3_reorder_timing,
    4: lever_4_prioritize_orders,
    5: lever_5_pricing_promo,
}


def evaluate_lever(lever: int, event_id: str, params: dict) -> dict:
    fn = LEVER_FUNCS.get(lever)
    if fn is None:
        return {"lever": lever, "cost": 0, "stockout_reduction": 0, "sla_impact": 0,
                "feasibility": 0, "description": "Unknown lever."}
    return fn(event_id, params or {})
