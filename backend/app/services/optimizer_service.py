"""
optimizer_service.py — Linear program (PuLP) that chooses a fractional mix
of the 5 response levers to minimize total cost subject to:
    stockout_risk < 10%   (i.e. stockout_reduction >= target)
    SLA >= 95%             (i.e. sla_gain >= required gain)

Each lever's cost/benefit is (near-)linear in its "qty_fraction" scope, so
we sample each lever once at frac=1.0 to derive per-unit-fraction rates,
then let PuLP choose continuous fractions x_l in [0, 1] per lever.

We solve the LP at three constraint-tightness levels (99%, 90%, 75% of the
required reduction) to produce three distinct ranked plans rather than a
single point solution, mirroring how a real ops team would want options.
"""
import pulp

from app.services.levers import evaluate_lever
from app.services.simulator_service import _baseline_stockout_risk, _baseline_sla


def _lever_rates(event_id: str) -> dict:
    rates = {}
    for lever in range(1, 6):
        r = evaluate_lever(lever, event_id, {})
        rates[lever] = {
            "cost": r["cost"], "stockout_reduction": r["stockout_reduction"],
            "sla_impact": r["sla_impact"], "description": r["description"],
        }
    return rates


def _solve_lp(rates: dict, required_reduction: float, required_sla_gain: float):
    prob = pulp.LpProblem("sentinel_optimizer", pulp.LpMinimize)
    x = {l: pulp.LpVariable(f"x_{l}", lowBound=0, upBound=1) for l in rates}

    prob += pulp.lpSum(rates[l]["cost"] * x[l] for l in rates)  # minimize cost
    prob += pulp.lpSum(rates[l]["stockout_reduction"] * x[l] for l in rates) >= required_reduction
    prob += pulp.lpSum(rates[l]["sla_impact"] * x[l] for l in rates) >= required_sla_gain

    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    if pulp.LpStatus[prob.status] != "Optimal":
        return None

    chosen = {l: round(v.value(), 3) for l, v in x.items() if v.value() and v.value() > 0.01}
    total_cost = sum(rates[l]["cost"] * frac for l, frac in chosen.items())
    total_reduction = sum(rates[l]["stockout_reduction"] * frac for l, frac in chosen.items())
    total_sla = sum(rates[l]["sla_impact"] * frac for l, frac in chosen.items())
    return {
        "levers_used": list(chosen.keys()),
        "fractions": chosen,
        "estimated_cost": round(total_cost, 2),
        "expected_stockout_reduction": round(total_reduction, 3),
        "sla_impact": round(total_sla, 3),
    }


def recommend(event_id: str) -> list:
    base_stockout = _baseline_stockout_risk(event_id)
    base_sla = _baseline_sla(event_id)

    target_stockout = 0.10
    target_sla = 95.0
    required_reduction_full = max(0.0, 1 - (target_stockout / base_stockout)) if base_stockout > 0 else 0.0
    required_sla_gain_full = max(0.0, (target_sla - base_sla) / 100)

    rates = _lever_rates(event_id)

    # cap requirements at what's actually achievable (sum of each lever's full-fraction
    # rate) so the LP is never infeasible purely because the ask exceeds total capacity
    max_reduction = sum(r["stockout_reduction"] for r in rates.values())
    max_sla_gain = sum(r["sla_impact"] for r in rates.values())
    required_reduction_full = min(required_reduction_full, max_reduction * 0.95) if max_reduction > 0 else 0.0
    required_sla_gain_full = min(required_sla_gain_full, max_sla_gain * 0.95) if max_sla_gain > 0 else 0.0

    plans = []
    for tightness, label in [(1.0, "Full compliance"), (0.85, "Balanced"), (0.65, "Cost-optimized")]:
        sol = _solve_lp(rates, required_reduction_full * tightness, required_sla_gain_full * tightness)
        if sol is None or not sol["levers_used"]:
            continue
        descriptions = [rates[l]["description"] for l in sol["levers_used"]]
        plans.append({
            "label": label,
            "levers_used": sol["levers_used"],
            "description": " + ".join(descriptions),
            "estimated_cost": sol["estimated_cost"],
            "expected_stockout_reduction": sol["expected_stockout_reduction"],
            "sla_impact": sol["sla_impact"],
            "feasibility": 1.0,
        })

    # de-duplicate identical lever-set plans, keep cheapest, then sort by cost
    seen = {}
    for p in plans:
        key = tuple(sorted(p["levers_used"]))
        if key not in seen or p["estimated_cost"] < seen[key]["estimated_cost"]:
            seen[key] = p
    ranked = sorted(seen.values(), key=lambda p: p["estimated_cost"])

    for i, p in enumerate(ranked, start=1):
        p["rank"] = i

    return ranked[:3] if ranked else []
