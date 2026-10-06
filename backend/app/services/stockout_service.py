import os
import joblib
import numpy as np
import pandas as pd

from app.config import MODEL_DIR
from app.db import get_store

_bundle = joblib.load(os.path.join(MODEL_DIR, "stockout_model.pkl"))
_MODEL = _bundle["model"]
_FEATURES = _bundle["feature_cols"]


def _feature_frame() -> pd.DataFrame:
    store = get_store()
    inventory = store.get_table("inventory")
    products = store.get_table("products")
    demand = store.get_table("demand_history")

    demand_stats = demand.groupby("product_id")["quantity"].agg(["mean", "std"]).rename(
        columns={"mean": "avg_daily_demand", "std": "demand_std"})
    df = inventory.merge(products, on="product_id").merge(demand_stats, on="product_id", how="left")
    df["demand_std"] = df["demand_std"].fillna(df["avg_daily_demand"] * 0.2)
    df["avg_daily_demand"] = df["avg_daily_demand"].fillna(1.0)
    df["days_of_cover"] = np.where(df["avg_daily_demand"] > 0,
                                    df["quantity_on_hand"] / df["avg_daily_demand"], 999)
    return df


def score_all() -> pd.DataFrame:
    df = _feature_frame()
    X = df[_FEATURES]
    proba = _MODEL.predict_proba(X)[:, 1]
    df["stockout_probability"] = proba
    return df


def get_stockout_risk(product_id: str) -> list:
    df = score_all()
    rows = df[df.product_id == product_id]
    out = []
    for _, r in rows.iterrows():
        out.append({
            "product_id": product_id,
            "warehouse_id": r.warehouse_id,
            "stockout_probability": round(float(r.stockout_probability), 3),
            "days_to_stockout": round(float(r.days_of_cover), 1) if r.days_of_cover < 999 else None,
        })
    return out
