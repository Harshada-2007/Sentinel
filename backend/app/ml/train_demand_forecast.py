"""
train_demand_forecast.py — XGBoost regressor forecasting next-day demand
using lag features (lag1, lag7, lag14, rolling means). At inference time the
service recursively forecasts 14 days ahead per product.
"""
import os
import joblib
import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.dummy import DummyRegressor

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "saved_models")
os.makedirs(MODEL_DIR, exist_ok=True)
SEED = 42

demand = pd.read_csv(os.path.join(DATA_DIR, "demand_history.csv"), parse_dates=["date"])
demand = demand.sort_values(["product_id", "date"])


def build_features(g):
    g = g.copy()
    g["lag1"] = g["quantity"].shift(1)
    g["lag7"] = g["quantity"].shift(7)
    g["lag14"] = g["quantity"].shift(14)
    g["roll_mean_7"] = g["quantity"].shift(1).rolling(7).mean()
    g["roll_mean_14"] = g["quantity"].shift(1).rolling(14).mean()
    g["dow"] = g["date"].dt.dayofweek
    g["day_of_month"] = g["date"].dt.day
    return g


feat_frames = [build_features(g) for _, g in demand.groupby("product_id")]
feat_df = pd.concat(feat_frames).dropna()

feature_cols = ["lag1", "lag7", "lag14", "roll_mean_7", "roll_mean_14", "dow", "day_of_month"]
X = feat_df[feature_cols]
y = feat_df["quantity"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED)

model = XGBRegressor(
    n_estimators=300, max_depth=5, learning_rate=0.05,
    subsample=0.8, colsample_bytree=0.8, random_state=SEED,
    objective="reg:squarederror",
)
model.fit(X_train, y_train)

preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)
r2 = r2_score(y_test, preds)

baseline = DummyRegressor(strategy="mean")
baseline.fit(X_train, y_train)
base_preds = baseline.predict(X_test)
base_mae = mean_absolute_error(y_test, base_preds)
base_r2 = r2_score(y_test, base_preds)

# naive lag1-as-prediction baseline (common demand forecasting baseline)
naive_mae = mean_absolute_error(y_test, X_test["lag1"])

print("=== Demand Forecast Model (XGBoost) ===")
print(f"Train rows: {len(X_train)}  Test rows: {len(X_test)}")
print(f"Model         -> MAE: {mae:.2f}  R2: {r2:.3f}")
print(f"Mean baseline -> MAE: {base_mae:.2f}  R2: {base_r2:.3f}")
print(f"Naive (lag1)  -> MAE: {naive_mae:.2f}")
print("Feature importances:")
for feat, imp in sorted(zip(feature_cols, model.feature_importances_), key=lambda x: -x[1]):
    print(f"  {feat:16s} {imp:.3f}")

joblib.dump({"model": model, "feature_cols": feature_cols}, os.path.join(MODEL_DIR, "demand_forecast_model.pkl"))
print(f"Saved -> {os.path.join(MODEL_DIR, 'demand_forecast_model.pkl')}")
