from app.services.levers import evaluate_lever
from app.services.impact_service import compute_impact
from app.services import stockout_service


def _baseline_stockout_risk(event_id: str) -> float:
    """Average stockout probability across products affected by this event."""
    impact = compute_impact(event_id)
    if not impact or not impact["affected_products"]:
        return 0.0
    scored = stockout_service.score_all()
    pids = [p["product_id"] for p in impact["affected_products"]]
    subset = scored[scored.product_id.isin(pids)]
    if subset.empty:
        return 0.0
    return float(subset["stockout_probability"].mean())


def _baseline_sla(event_id: str) -> float:
    impact = compute_impact(event_id)
    if not impact:
        return 100.0
    # naive: SLA erodes with severity and number of affected orders
    severity = impact["cascade"]["event"]["severity"]
    order_factor = min(1.0, impact["affected_orders_count"] / 500)
    erosion = severity * 35 + order_factor * 20
    return max(40.0, 100.0 - erosion)


def run_simulation(event_id: str, actions: list) -> dict:
    base_stockout = _baseline_stockout_risk(event_id)
    base_sla = _baseline_sla(event_id)

    do_nothing = {
        "stockout_risk_pct": round(base_stockout * 100, 1),
        "sla_pct": round(base_sla, 1),
        "total_cost": 0.0,
        "details": [{"description": "No action taken — disruption proceeds unmitigated."}],
    }

    total_cost = 0.0
    total_stockout_reduction = 0.0
    total_sla_gain = 0.0
    details = []
    for action in actions:
        result = evaluate_lever(action.lever, event_id, action.params)
        total_cost += result["cost"]
        total_stockout_reduction += result["stockout_reduction"]
        total_sla_gain += result["sla_impact"]
        details.append(result)

    new_stockout = max(0.02, base_stockout * (1 - min(0.95, total_stockout_reduction)))
    new_sla = min(99.9, base_sla + total_sla_gain * 100)

    with_actions = {
        "stockout_risk_pct": round(new_stockout * 100, 1),
        "sla_pct": round(new_sla, 1),
        "total_cost": round(total_cost, 2),
        "details": details,
    }

    return {"event_id": event_id, "do_nothing": do_nothing, "with_actions": with_actions}
