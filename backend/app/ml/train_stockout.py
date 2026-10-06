"""
train_stockout.py — RandomForest classifier: P(stockout within 7 days) per
product-warehouse, trained on simulated depletion trajectories derived from
actual inventory levels + demand history statistics.
"""
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.dummy import DummyClassifier

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "saved_models")
os.makedirs(MODEL_DIR, exist_ok=True)
SEED = 42
np.random.seed(SEED)

inventory = pd.read_csv(os.path.join(DATA_DIR, "inventory.csv"))
products = pd.read_csv(os.path.join(DATA_DIR, "products.csv"))
demand = pd.read_csv(os.path.join(DATA_DIR, "demand_history.csv"))

demand_stats = demand.groupby("product_id")["quantity"].agg(["mean", "std"]).rename(
    columns={"mean": "avg_daily_demand", "std": "demand_std"})
inv = inventory.merge(products, on="product_id").merge(demand_stats, on="product_id")
inv["demand_std"] = inv["demand_std"].fillna(inv["avg_daily_demand"] * 0.2)

rows = []
N_SIM_PER_ROW = 6
for _, r in inv.iterrows():
    for _ in range(N_SIM_PER_ROW):
        # simulate 7 days of stochastic demand draws and see if stock runs out
        daily_demand = np.clip(np.random.normal(r.avg_daily_demand, r.demand_std, size=7), 0, None)
        incoming = r.quantity_in_transit if np.random.rand() < 0.5 else 0
        stock = r.quantity_on_hand + incoming * np.random.uniform(0, 1)
        cumulative = np.cumsum(daily_demand)
        stockout = bool((stock - cumulative < 0).any())
        rows.append({
            "quantity_on_hand": r.quantity_on_hand,
            "quantity_in_transit": r.quantity_in_transit,
            "safety_stock": r.safety_stock,
            "reorder_point": r.reorder_point,
            "lead_time_days": r.lead_time_days,
            "avg_daily_demand": r.avg_daily_demand,
            "demand_std": r.demand_std,
            "days_of_cover": (r.quantity_on_hand / r.avg_daily_demand) if r.avg_daily_demand > 0 else 999,
            "stockout_in_7d": int(stockout),
        })

df = pd.DataFrame(rows)
feature_cols = ["quantity_on_hand", "quantity_in_transit", "safety_stock", "reorder_point",
                "lead_time_days", "avg_daily_demand", "demand_std", "days_of_cover"]
X = df[feature_cols]
y = df["stockout_in_7d"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=SEED, stratify=y)

model = RandomForestClassifier(n_estimators=300, max_depth=8, min_samples_leaf=5,
                                random_state=SEED, class_weight="balanced")
model.fit(X_train, y_train)

preds = model.predict(X_test)
proba = model.predict_proba(X_test)[:, 1]
acc = accuracy_score(y_test, preds)
f1 = f1_score(y_test, preds)
auc = roc_auc_score(y_test, proba) if len(set(y_test)) > 1 else float("nan")

baseline = DummyClassifier(strategy="most_frequent", random_state=SEED)
baseline.fit(X_train, y_train)
base_preds = baseline.predict(X_test)
base_acc = accuracy_score(y_test, base_preds)
base_f1 = f1_score(y_test, base_preds, zero_division=0)

print("=== Stockout Prediction Model (RandomForest) ===")
print(f"Train rows: {len(X_train)}  Test rows: {len(X_test)}")
print(f"Model    -> accuracy: {acc:.3f}  f1: {f1:.3f}  auc: {auc:.3f}")
print(f"Baseline -> accuracy: {base_acc:.3f}  f1: {base_f1:.3f}  (majority-class predictor)")
print("Feature importances:")
for feat, imp in sorted(zip(feature_cols, model.feature_importances_), key=lambda x: -x[1]):
    print(f"  {feat:20s} {imp:.3f}")

joblib.dump({"model": model, "feature_cols": feature_cols}, os.path.join(MODEL_DIR, "stockout_model.pkl"))
print(f"Saved -> {os.path.join(MODEL_DIR, 'stockout_model.pkl')}")
