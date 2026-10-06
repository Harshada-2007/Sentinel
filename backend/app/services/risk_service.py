import os
import joblib
import pandas as pd

from app.config import MODEL_DIR
from app.db import get_store

_bundle = joblib.load(os.path.join(MODEL_DIR, "supplier_risk_model.pkl"))
_MODEL = _bundle["model"]
_FEATURES = _bundle["feature_cols"]


def _build_features_for_suppliers(suppliers: pd.DataFrame, events: pd.DataFrame) -> pd.DataFrame:
    """Build the full feature set the model expects."""
    if events.empty:
        sev_map, cnt_map = {}, {}
    else:
        sev_map = events.groupby("affected_supplier_id")["severity"].max().to_dict()
        cnt_map = events.groupby("affected_supplier_id").size().to_dict()

    df = suppliers.copy()

    # base features
    df["recent_event_severity"] = df["supplier_id"].map(sev_map).fillna(0.0)
    df["recent_event_count"] = df["supplier_id"].map(cnt_map).fillna(0).astype(int)

    # engineered interaction features (must match training)
    df["tier_x_reliability"] = df["tier"] * df["reliability_score"]

    df["lead_time_category"] = df["lead_time_days"].apply(
        lambda x: 0 if x < 15 else 1 if x < 30 else 2
    )

    df["event_impact"] = df["recent_event_severity"] * df["recent_event_count"].clip(lower=1)

    return df


def _risk_tier(p: float) -> str:
    if p >= 0.66:
        return "critical"
    if p >= 0.35:
        return "warning"
    return "ok"


def score_all_suppliers() -> pd.DataFrame:
    store = get_store()
    suppliers = store.get_table("suppliers")
    events = store.get_table("disruption_events")
    feat_df = _build_features_for_suppliers(suppliers, events)
    X = feat_df[_FEATURES]
    proba = _MODEL.predict_proba(X)[:, 1]
    feat_df["risk_score"] = proba
    feat_df["risk_tier"] = feat_df["risk_score"].apply(_risk_tier)
    return feat_df


def get_supplier_risk(supplier_id: str) -> dict:
    store = get_store()
    suppliers = store.get_table("suppliers")
    events = store.get_table("disruption_events")
    row = suppliers[suppliers.supplier_id == supplier_id]
    if row.empty:
        return None
    feat_df = _build_features_for_suppliers(row, events)
    X = feat_df[_FEATURES]
    proba = float(_MODEL.predict_proba(X)[:, 1][0])

    importances = list(zip(_FEATURES, _MODEL.feature_importances_))
    importances.sort(key=lambda x: -x[1])
    top_factors = [
        {"factor": f, "importance": round(float(i), 3), "value": float(feat_df.iloc[0][f])}
        for f, i in importances[:4]
    ]

    supplier = row.iloc[0]
    sev = float(feat_df.iloc[0]["recent_event_severity"])
    explanation = (
        f"{supplier['name']} ({supplier.location}) has a {proba*100:.0f}% probability of a delay "
        f"greater than 2 days, driven primarily by its reliability score "
        f"({supplier.reliability_score:.2f}) and lead time ({int(supplier.lead_time_days)} days)."
    )
    if sev > 0:
        explanation += f" A recent disruption event (severity {sev:.2f}) is elevating this risk further."

    return {
        "supplier_id": supplier_id,
        "delay_probability": round(proba, 3),
        "risk_tier": _risk_tier(proba),
        "explanation": explanation,
        "top_factors": top_factors,
    }