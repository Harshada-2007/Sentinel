from app.config import OPENAI_API_KEY
from app.services.impact_service import compute_impact
from app.services.risk_service import get_supplier_risk
from app.services.optimizer_service import recommend


def _rule_based_explanation(event_id: str, action_plan_rank: int = 1) -> str:
    impact = compute_impact(event_id)
    if not impact:
        return "Event not found."

    risk = get_supplier_risk(impact["affected_supplier"].get("supplier_id", "")) or {}
    plans = recommend(event_id)
    plan = next((p for p in plans if p["rank"] == action_plan_rank), plans[0] if plans else None)

    supplier_name = impact["affected_supplier"].get("name", "the supplier")
    location = impact["affected_supplier"].get("location", "")
    top_product = impact["affected_products"][0] if impact["affected_products"] else None

    lines = []
    delay_prob_pct = f"{risk.get('delay_probability', 0) * 100:.0f}%" if risk else "an elevated"
    lines.append(
        f"{supplier_name} ({location}) has a {delay_prob_pct} probability of a "
        f"{impact['cascade']['event']['predicted_delay_days']}-day delay due to a "
        f"{impact['cascade']['event']['event_type'].replace('_', ' ')}."
    )
    if top_product:
        lines.append(
            f"This threatens {top_product['name']} ({top_product['product_id']}), affecting "
            f"{impact['affected_orders_count']} open orders worth ₹{impact['revenue_at_risk']:,.0f}."
        )
    if plan:
        lines.append(
            f"The recommended plan ({plan['label']}) combines lever(s) {plan['levers_used']}: "
            f"{plan['description']}"
        )
        lines.append(
            f"Total cost: ₹{plan['estimated_cost']:,.0f}. This reduces stockout risk by "
            f"{plan['expected_stockout_reduction']*100:.0f}% and improves SLA compliance by "
            f"{plan['sla_impact']*100:.1f} points."
        )
    else:
        lines.append("No feasible mitigation plan could be found within current constraints.")

    return " ".join(lines)


def _llm_explanation(event_id: str, action_plan_rank: int = 1) -> str:
    """Uses the OpenAI API when OPENAI_API_KEY is configured; falls back to
    the rule-based template on any error so the demo never breaks."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)

        impact = compute_impact(event_id)
        risk = get_supplier_risk(impact["affected_supplier"].get("supplier_id", "")) or {}
        plans = recommend(event_id)
        plan = next((p for p in plans if p["rank"] == action_plan_rank), plans[0] if plans else None)

        prompt = (
            "You are a supply chain control tower assistant. Write a concise, 3-paragraph "
            "executive explanation (no markdown) of the disruption, its business impact, and "
            "the recommended action plan, using ONLY the facts below. All monetary values are "
            "in Indian rupees (INR); use ₹ or rupees and never use dollars or USD.\n\n"
            f"Impact: {impact}\nSupplier risk: {risk}\nRecommended plan: {plan}\n"
        )
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=350,
            temperature=0.4,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return _rule_based_explanation(event_id, action_plan_rank)


def generate_explanation(event_id: str, action_plan_rank: int = 1) -> str:
    if OPENAI_API_KEY:
        return _llm_explanation(event_id, action_plan_rank)
    return _rule_based_explanation(event_id, action_plan_rank)
