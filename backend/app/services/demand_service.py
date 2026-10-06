import os
import joblib
import numpy as np
import pandas as pd
from datetime import timedelta

from app.config import MODEL_DIR
from app.db import get_store

_bundle = joblib.load(os.path.join(MODEL_DIR, "demand_forecast_model.pkl"))
_MODEL = _bundle["model"]
_FEATURES = _bundle["feature_cols"]

HORIZON_DAYS = 14


def forecast_product(product_id: str) -> list:
    store = get_store()
    demand = store.get_table("demand_history")
    hist = demand[demand.product_id == product_id].copy()
    if hist.empty:
        return []
    hist["date"] = pd.to_datetime(hist["date"])
    hist = hist.sort_values("date")

    series = hist["quantity"].tolist()
    last_date = hist["date"].max()

    forecast = []
    for step in range(HORIZON_DAYS):
        next_date = last_date + timedelta(days=step + 1)
        lag1 = series[-1]
        lag7 = series[-7] if len(series) >= 7 else series[0]
        lag14 = series[-14] if len(series) >= 14 else series[0]
        roll_mean_7 = float(np.mean(series[-7:])) if len(series) >= 7 else float(np.mean(series))
        roll_mean_14 = float(np.mean(series[-14:])) if len(series) >= 14 else float(np.mean(series))
        row = pd.DataFrame([{
            "lag1": lag1, "lag7": lag7, "lag14": lag14,
            "roll_mean_7": roll_mean_7, "roll_mean_14": roll_mean_14,
            "dow": next_date.dayofweek, "day_of_month": next_date.day,
        }])[_FEATURES]
        pred = max(0.0, float(_MODEL.predict(row)[0]))
        series.append(pred)
        forecast.append({"date": next_date.date().isoformat(), "predicted_quantity": round(pred, 1)})

    return forecast


def forecast_all(product_ids=None) -> dict:
    store = get_store()
    products = store.get_table("products")
    ids = product_ids or products["product_id"].tolist()
    return {pid: forecast_product(pid) for pid in ids}
