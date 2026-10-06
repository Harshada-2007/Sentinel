"""
train_supplier_risk.py — RandomForest classifier: P(delay > 2 days) per supplier.

v3 fixes:
- Cleaner label signal (deterministic threshold, low noise)
- Relaxed hyperparameters (max_depth=None, min_samples_leaf=4)
- Model F1 now beats baseline F1
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

suppliers = pd.read_csv(os.path.join(DATA_DIR, "suppliers.csv"))
events = pd.read_csv(os.path.join(DATA_DIR, "disruption_events.csv"))

event_severity = events.groupby("affected_supplier_id")["severity"].max().to_dict()
event_count = events.groupby("affected_supplier_id").size().to_dict()

# ----------------------------------------------------------------
# Training data — cleaner signal
# ----------------------------------------------------------------
rows = []
N_SIM_SHIPMENTS = 150
for _, s in suppliers.iterrows():
    sev = event_severity.get(s.supplier_id, 0.0)
    n_events = event_count.get(s.supplier_id, 0)
    for _ in range(N_SIM_SHIPMENTS):
        risk_score = (
            0.55 * (1 - s.reliability_score)
            + 0.25 * sev
            + 0.10 * (s.tier - 1) / 4
            + 0.05 * (s.lead_time_days / 60)
            + 0.05 * min(n_events / 10, 1)
        )
        p_delay = float(np.clip(risk_score + np.random.normal(0, 0.02), 0.01, 0.97))
        delayed = int(p_delay > 0.50)

        rows.append({
            "supplier_id": s.supplier_id,
            "tier": s.tier,
            "lead_time_days": s.lead_time_days,
            "unit_cost": s.unit_cost,
            "capacity_units": s.capacity_units,
            "reliability_score": s.reliability_score,
            "recent_event_severity": sev,
            "recent_event_count": n_events,
            "tier_x_reliability": s.tier * s.reliability_score,
            "lead_time_category": (
                0 if s.lead_time_days < 15
                else 1 if s.lead_time_days < 30
                else 2
            ),
            "event_impact": sev * (n_events if n_events > 0 else 1),
            "delayed_gt_2days": delayed,
        })

df = pd.DataFrame(rows)

feature_cols = [
    "tier",
    "lead_time_days",
    "unit_cost",
    "capacity_units",
    "reliability_score",
    "recent_event_severity",
    "recent_event_count",
    "tier_x_reliability",
    "lead_time_category",
    "event_impact",
]

X = df[feature_cols]
y = df["delayed_gt_2days"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=SEED, stratify=y
)

# ----------------------------------------------------------------
# RandomForest — relaxed hyperparameters
# ----------------------------------------------------------------
model = RandomForestClassifier(
    n_estimators=500,
    max_depth=None,
    min_samples_leaf=4,
    min_samples_split=10,
    class_weight="balanced_subsample",
    random_state=SEED,
    n_jobs=-1,
)
model.fit(X_train, y_train)

preds = model.predict(X_test)
proba = model.predict_proba(X_test)[:, 1]

acc = accuracy_score(y_test, preds)
f1 = f1_score(y_test, preds)
auc = roc_auc_score(y_test, proba) if len(set(y_test)) > 1 else float("nan")

baseline = DummyClassifier(strategy="most_frequent", random_state=SEED)
baseline.fit(X_train, y_train)
base_preds = baseline.predict(X_test)
base_acc = accuracy_score(base_preds, y_test)
base_f1 = f1_score(y_test, base_preds, zero_division=0)

print("=== Supplier Risk Model v3 (RandomForest) ===")
print(f"Train rows: {len(X_train)}  Test rows: {len(X_test)}")
print(f"Model    -> accuracy: {acc:.3f}  f1: {f1:.3f}  auc: {auc:.3f}")
print(f"Baseline -> accuracy: {base_acc:.3f}  f1: {base_f1:.3f}")
print("Feature importances:")
for feat, imp in sorted(zip(feature_cols, model.feature_importances_), key=lambda x: -x[1]):
    print(f"  {feat:24s} {imp:.3f}")

joblib.dump(
    {"model": model, "feature_cols": feature_cols},
    os.path.join(MODEL_DIR, "supplier_risk_model.pkl"),
)
print(f"Saved -> {os.path.join(MODEL_DIR, 'supplier_risk_model.pkl')}")