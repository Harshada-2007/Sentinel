"""
generate_data.py — MEGA SYNTHETIC SUPPLY CHAIN GENERATOR
Sentinel Control Tower

Produces:
  - 200 suppliers in a 5-tier supply chain
  - 300 products
  - 15 warehouses (India-focused)
  - ~3,500 inventory rows
  - 25,000 orders
  - 600 disruption events + 7 hand-crafted demo scenarios
  - 365-day demand history
  - All monetary values in INR (₹)

Run: python data/generate_data.py
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

OUT_DIR = os.path.dirname(__file__)
os.makedirs(OUT_DIR, exist_ok=True)

TODAY = datetime(2026, 9, 28)
USD_TO_INR = 83.0

# ==================================================================
# CONFIG
# ==================================================================
N_SUPPLIERS = 200
N_PRODUCTS = 300
N_WAREHOUSES = 15
N_ORDERS = 25000
N_RANDOM_EVENTS = 593   # + 7 handcrafted = 600 total
DEMAND_HISTORY_DAYS = 365

REGIONS = [
    "Shenzhen, CN", "Shanghai, CN", "Taipei, TW", "Hsinchu, TW",
    "Hamburg, DE", "Rotterdam, NL", "Perth, AU", "Busan, KR",
    "Ho Chi Minh, VN", "Hanoi, VN", "Mumbai, IN", "Chennai, IN",
    "Bengaluru, IN", "Pune, IN", "Houston, US", "Monterrey, MX",
    "Sao Paulo, BR", "Guadalajara, MX", "Penang, MY", "Bangkok, TH",
]

SUPPLIER_PREFIXES = [
    "Alpha", "Beta", "Gamma", "Delta", "Omega", "Nova", "Vertex",
    "Orion", "Zenith", "Atlas", "Titan", "Helios", "Quantum",
    "Fusion", "Nexus", "Apex", "Prime", "Sigma", "Theta", "Kappa",
]
SUPPLIER_SUFFIXES = [
    "Components", "Electronics", "Materials", "Industries",
    "Supply Co", "Manufacturing", "Logistics", "Systems",
    "Technologies", "Works",
]

CATEGORIES = [
    "Electronics", "Fasteners", "Packaging", "Plastics",
    "Textiles", "Metals", "Chemicals", "Machinery",
]

PRODUCT_PREFIXES = [
    "SmartHub", "FlexMount", "CoreDrive", "PowerCell", "LinkNode",
    "SensePad", "TorqueArm", "FlowValve", "RailKit", "HeatSink",
    "SignalBox", "VoltPack", "GridLock", "AeroFin", "MicroGear",
]
PRODUCT_SUFFIXES = [
    "Controller", "Bracket", "Module", "Unit", "Kit",
    "Assembly", "Panel", "Sensor", "Actuator", "Housing",
]

EVENT_TYPES = [
    "port_strike", "factory_fire", "weather", "customs_delay",
    "labor_dispute", "raw_material_shortage", "geopolitical",
    "logistics_failure",
]

CUSTOMER_TIERS = ["A", "B", "C"]
ORDER_STATUSES = ["pending", "in_transit", "delivered", "delayed", "cancelled"]

WAREHOUSE_CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Chennai", "Pune",
    "Hyderabad", "Kolkata", "Ahmedabad", "Jaipur", "Kochi",
    "Lucknow", "Coimbatore", "Nagpur", "Indore", "Surat",
]

# ==================================================================
# 1. SUPPLIERS — 5 tiers, realistic names, INR costs
# ==================================================================
print("Generating suppliers...")

suppliers = []
tier_distribution = [0.15, 0.25, 0.25, 0.20, 0.15]  # tiers 1..5

for i in range(1, N_SUPPLIERS + 1):
    tier = int(np.random.choice([1, 2, 3, 4, 5], p=tier_distribution))

    # reliability decreases with tier depth
    base_reliability = {
        1: 0.88, 2: 0.82, 3: 0.75, 4: 0.70, 5: 0.65
    }[tier]
    reliability = float(np.clip(np.random.normal(base_reliability, 0.10), 0.30, 0.99))

    # lead time increases with tier depth
    base_lead = {1: 14, 2: 20, 3: 26, 4: 32, 5: 40}[tier]
    lead_time = int(np.clip(np.random.normal(base_lead, 6), 2, 90))

    # unit cost in INR (₹125–₹20,750 range, converted from USD 1.5–250)
    unit_cost = round(float(np.random.uniform(1.5, 250)) * USD_TO_INR, 2)

    capacity = int(np.random.uniform(2000, 50000))

    suppliers.append({
        "supplier_id": f"SUP{i:03d}",
        "name": f"{random.choice(SUPPLIER_PREFIXES)} {random.choice(SUPPLIER_SUFFIXES)}",
        "tier": tier,
        "location": random.choice(REGIONS),
        "lead_time_days": lead_time,
        "unit_cost": unit_cost,
        "capacity_units": capacity,
        "reliability_score": round(reliability, 3),
        "backup_for": None,
    })

suppliers_df = pd.DataFrame(suppliers)

# Add backup relationships: 30% of non-Tier-1 suppliers become backups for Tier-1 suppliers
tier1_ids = suppliers_df[suppliers_df.tier == 1].supplier_id.tolist()
candidates = suppliers_df[suppliers_df.tier != 1].sample(frac=0.30, random_state=SEED).index
for idx in candidates:
    suppliers_df.loc[idx, "backup_for"] = random.choice(tier1_ids)

print(f"  → {len(suppliers_df)} suppliers across 5 tiers")

# ==================================================================
# 2. PRODUCTS — 300 SKUs, each mapped to a Tier-1 supplier
# ==================================================================
print("Generating products...")

tier1_suppliers = suppliers_df[suppliers_df.tier == 1]
products = []
for i in range(1, N_PRODUCTS + 1):
    sup = tier1_suppliers.sample(1, random_state=SEED + i).iloc[0]
    unit_cost = round(float(np.random.uniform(2, 300)) * USD_TO_INR, 2)
    unit_price = round(unit_cost * float(np.random.uniform(1.3, 2.2)), 2)

    products.append({
        "product_id": f"P{i:03d}",
        "name": f"{random.choice(PRODUCT_PREFIXES)} {random.choice(PRODUCT_SUFFIXES)}",
        "category": random.choice(CATEGORIES),
        "unit_price": unit_price,
        "unit_cost": unit_cost,
        "safety_stock": int(np.random.uniform(50, 500)),
        "reorder_point": int(np.random.uniform(100, 800)),
        "lead_time_days": int(sup.lead_time_days),
        "supplier_id": sup.supplier_id,
    })

products_df = pd.DataFrame(products)
print(f"  → {len(products_df)} products")

# ==================================================================
# 3. WAREHOUSES — 15 across India, INR holding costs
# ==================================================================
print("Generating warehouses...")

warehouses = []
for i, city in enumerate(WAREHOUSE_CITIES, start=1):
    warehouses.append({
        "warehouse_id": f"WH{i:02d}",
        "name": f"{city} DC",
        "location": f"{city}, IN",
        "capacity_units": int(np.random.uniform(20000, 100000)),
        # ₹0.83–₹6.64 per unit per day (converted from $0.01–0.08)
        "holding_cost_per_unit_day": round(float(np.random.uniform(0.83, 6.64)), 2),
    })

warehouses_df = pd.DataFrame(warehouses)
print(f"  → {len(warehouses_df)} warehouses")

# ==================================================================
# 4. INVENTORY — Product × Warehouse where stock exists
# ==================================================================
print("Generating inventory...")

inventory_rows = []
inv_id = 1
for _, p in products_df.iterrows():
    for _, w in warehouses_df.iterrows():
        if np.random.rand() < 0.65:   # ~65% of pairs have stock
            qoh = int(np.random.uniform(0, p.reorder_point * 2.5))
            inventory_rows.append({
                "inventory_id": f"INV{inv_id:06d}",
                "product_id": p.product_id,
                "warehouse_id": w.warehouse_id,
                "quantity_on_hand": qoh,
                "quantity_in_transit": int(np.random.uniform(0, 300)),
                "last_updated": (TODAY - timedelta(days=int(np.random.uniform(0, 5)))).date().isoformat(),
            })
            inv_id += 1

inventory_df = pd.DataFrame(inventory_rows)
print(f"  → {len(inventory_df)} inventory rows")

# ==================================================================
# 5. ORDERS — 25,000 across all product-warehouse pairs
# ==================================================================
print("Generating orders...")

orders_rows = []
valid_pairs = inventory_df[["product_id", "warehouse_id"]].values
lead_time_lookup = products_df.set_index("product_id")["lead_time_days"].to_dict()

for i in range(1, N_ORDERS + 1):
    pid, wid = valid_pairs[np.random.randint(0, len(valid_pairs))]
    tier = np.random.choice(CUSTOMER_TIERS, p=[0.20, 0.35, 0.45])
    order_date = TODAY - timedelta(days=int(np.random.uniform(0, 60)))
    lead = lead_time_lookup[pid]
    promised = order_date + timedelta(days=lead + int(np.random.uniform(-2, 5)))

    priority = {
        "A": float(np.random.uniform(0.7, 1.0)),
        "B": float(np.random.uniform(0.4, 0.75)),
        "C": float(np.random.uniform(0.1, 0.45)),
    }[tier]

    orders_rows.append({
        "order_id": f"ORD{i:06d}",
        "product_id": pid,
        "warehouse_id": wid,
        "customer_id": f"CUST{int(np.random.uniform(1, 900)):04d}",
        "customer_tier": tier,
        "quantity": int(np.random.uniform(5, 400)),
        "order_date": order_date.date().isoformat(),
        "promised_delivery_date": promised.date().isoformat(),
        "priority_score": round(priority, 3),
        "status": np.random.choice(ORDER_STATUSES, p=[0.15, 0.35, 0.35, 0.10, 0.05]),
    })

orders_df = pd.DataFrame(orders_rows)
print(f"  → {len(orders_df)} orders")

# ==================================================================
# 6. DISRUPTION EVENTS — 7 handcrafted + 593 random
# ==================================================================
print("Generating disruption events...")

# --- 7 handcrafted demo scenarios ---
# Pick suppliers that definitely exist
tier1_ids = suppliers_df[suppliers_df.tier == 1].supplier_id.tolist()
tier2_ids = suppliers_df[suppliers_df.tier == 2].supplier_id.tolist()
tier3_ids = suppliers_df[suppliers_df.tier == 3].supplier_id.tolist()

handcrafted = [
    {
        "event_id": "EVT001",
        "event_type": "port_strike",
        "affected_supplier_id": tier1_ids[0],
        "affected_region": "Shenzhen, CN",
        "detected_date": (TODAY - timedelta(days=3)).date().isoformat(),
        "severity": 0.82,
        "predicted_delay_days": 6,
        "source": "news_feed",
        "description": "Port strike at Shenzhen halts container loading for 6 days. 40+ vessels queued.",
    },
    {
        "event_id": "EVT002",
        "event_type": "factory_fire",
        "affected_supplier_id": tier2_ids[0],
        "affected_region": "Hsinchu, TW",
        "detected_date": (TODAY - timedelta(days=4)).date().isoformat(),
        "severity": 0.91,
        "predicted_delay_days": 14,
        "source": "news_feed",
        "description": "Major fire at Delta Chips fab. Production halted; recovery estimated at 2 weeks.",
    },
    {
        "event_id": "EVT003",
        "event_type": "weather",
        "affected_supplier_id": tier1_ids[1] if len(tier1_ids) > 1 else tier1_ids[0],
        "affected_region": "Hamburg, DE",
        "detected_date": (TODAY - timedelta(days=3)).date().isoformat(),
        "severity": 0.62,
        "predicted_delay_days": 3,
        "source": "weather_service",
        "description": "Severe North Sea storm. Port of Hamburg at 40% capacity for 3 days.",
    },
    {
        "event_id": "EVT004",
        "event_type": "customs_delay",
        "affected_supplier_id": tier1_ids[2] if len(tier1_ids) > 2 else tier1_ids[0],
        "affected_region": "Chennai, IN",
        "detected_date": (TODAY - timedelta(days=5)).date().isoformat(),
        "severity": 0.55,
        "predicted_delay_days": 5,
        "source": "customs_alert",
        "description": "Customs backlog at Chennai port. Average clearance time up from 2 to 7 days.",
    },
    {
        "event_id": "EVT005",
        "event_type": "labor_dispute",
        "affected_supplier_id": tier1_ids[0],
        "affected_region": "Shenzhen, CN",
        "detected_date": (TODAY - timedelta(days=3)).date().isoformat(),
        "severity": 0.71,
        "predicted_delay_days": 8,
        "source": "news_feed",
        "description": "Truck drivers at Shenzhen logistics hub strike. Inland transport frozen.",
    },
    {
        "event_id": "EVT006",
        "event_type": "raw_material_shortage",
        "affected_supplier_id": tier3_ids[0],
        "affected_region": "Perth, AU",
        "detected_date": (TODAY - timedelta(days=6)).date().isoformat(),
        "severity": 0.68,
        "predicted_delay_days": 10,
        "source": "supplier_api",
        "description": "Lithium ore shortage in Western Australia. Downstream Tier-1 suppliers impacted.",
    },
    {
        "event_id": "EVT007",
        "event_type": "geopolitical",
        "affected_supplier_id": tier1_ids[0],
        "affected_region": "Rotterdam, NL",
        "detected_date": (TODAY - timedelta(days=2)).date().isoformat(),
        "severity": 0.78,
        "predicted_delay_days": 12,
        "source": "news_feed",
        "description": "Trade sanctions announced. All shipments from this region require re-routing.",
    },
]

# --- 593 random events ---
random_events = []
for i in range(1, N_RANDOM_EVENTS + 1):
    sup = suppliers_df.sample(1, random_state=SEED + 1000 + i).iloc[0]
    severity = round(float(np.clip(np.random.beta(2, 3), 0.05, 0.99)), 3)
    detected = TODAY - timedelta(days=int(np.random.uniform(0, 45)))
    random_events.append({
        "event_id": f"EVT{100 + i:04d}",
        "event_type": random.choice(EVENT_TYPES),
        "affected_supplier_id": sup.supplier_id,
        "affected_region": sup.location,
        "detected_date": detected.date().isoformat(),
        "severity": severity,
        "predicted_delay_days": int(np.clip(np.random.normal(severity * 10, 2), 1, 30)),
        "source": random.choice(["news_feed", "supplier_api", "weather_service", "customs_alert", "manual_entry"]),
        "description": f"{random.choice(EVENT_TYPES).replace('_', ' ').title()} reported near {sup.location} affecting {sup['name']}.",
    })

events_df = pd.DataFrame(handcrafted + random_events)
print(f"  → {len(events_df)} disruption events (7 seeded scenarios + {N_RANDOM_EVENTS} random)")

# ==================================================================
# 7. DEMAND HISTORY — 365 days per product
# ==================================================================
print("Generating demand history (this may take a moment)...")

demand_rows = []
row_id = 1
for _, p in products_df.iterrows():
    base = np.random.uniform(20, 200)
    trend = np.random.uniform(-0.05, 0.15)
    for d in range(DEMAND_HISTORY_DAYS):
        date = TODAY - timedelta(days=DEMAND_HISTORY_DAYS - d)
        weekly = 1 + 0.20 * np.sin(2 * np.pi * d / 7)
        monthly = 1 + 0.15 * np.sin(2 * np.pi * d / 30)
        yearly = 1 + 0.10 * np.sin(2 * np.pi * d / 365)
        noise = np.random.normal(1, 0.12)
        qty = max(0, base * (1 + trend * d / DEMAND_HISTORY_DAYS) * weekly * monthly * yearly * noise)
        demand_rows.append({
            "id": row_id,
            "product_id": p.product_id,
            "date": date.date().isoformat(),
            "quantity": int(round(qty)),
        })
        row_id += 1

demand_df = pd.DataFrame(demand_rows)
print(f"  → {len(demand_df)} demand rows")

# ==================================================================
# WRITE CSVs
# ==================================================================
print("\nWriting CSVs...")

suppliers_df.to_csv(os.path.join(OUT_DIR, "suppliers.csv"), index=False)
products_df.to_csv(os.path.join(OUT_DIR, "products.csv"), index=False)
warehouses_df.to_csv(os.path.join(OUT_DIR, "warehouses.csv"), index=False)
inventory_df.to_csv(os.path.join(OUT_DIR, "inventory.csv"), index=False)
orders_df.to_csv(os.path.join(OUT_DIR, "orders.csv"), index=False)
events_df.to_csv(os.path.join(OUT_DIR, "disruption_events.csv"), index=False)
demand_df.to_csv(os.path.join(OUT_DIR, "demand_history.csv"), index=False)

# ==================================================================
# SUMMARY
# ==================================================================
print("\n" + "=" * 60)
print("MEGA DATA GENERATION COMPLETE")
print("=" * 60)
print(f"  suppliers.csv          {len(suppliers_df):>7} rows")
print(f"  products.csv           {len(products_df):>7} rows")
print(f"  warehouses.csv         {len(warehouses_df):>7} rows")
print(f"  inventory.csv          {len(inventory_df):>7} rows")
print(f"  orders.csv             {len(orders_df):>7} rows")
print(f"  disruption_events.csv  {len(events_df):>7} rows")
print(f"  demand_history.csv     {len(demand_df):>7} rows")
print()
print("Seeded demo scenarios (click-through ready):")
for e in handcrafted:
    print(f"  {e['event_id']}  {e['event_type']:<22} {e['affected_region']:<18} sev={e['severity']}")
print()
print(f"Currency: INR (₹)  |  Exchange rate used: 1 USD = {USD_TO_INR} INR")
print("Next step: retrain models")
print("  python app/ml/train_supplier_risk.py")
print("  python app/ml/train_demand_forecast.py")
print("  python app/ml/train_stockout.py")
print("=" * 60)