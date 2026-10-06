"""
seed_supabase.py — Loads the CSVs produced by generate_data.py into the
Supabase tables created by supabase/schema.sql. Requires SUPABASE_URL and
SUPABASE_KEY to be set (see backend/.env.example).

Run: python data/seed_supabase.py
"""
import os
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

DATA_DIR = os.path.dirname(__file__)
BATCH_SIZE = 500

TABLES = [
    ("suppliers.csv", "suppliers"),
    ("products.csv", "products"),
    ("warehouses.csv", "warehouses"),
    ("inventory.csv", "inventory"),
    ("orders.csv", "orders"),
    ("disruption_events.csv", "disruption_events"),
    ("demand_history.csv", "demand_history"),
]


def main():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise SystemExit("SUPABASE_URL / SUPABASE_KEY not set — see backend/.env.example")

    client = create_client(url, key)

    for fname, table in TABLES:
        path = os.path.join(DATA_DIR, fname)
        if not os.path.exists(path):
            print(f"skip {table}: {fname} not found (run generate_data.py first)")
            continue
        df = pd.read_csv(path)
        # demand_history's 'id' column is auto-generated (bigserial) in Postgres
        if table == "demand_history" and "id" in df.columns:
            df = df.drop(columns=["id"])
        records = df.where(pd.notnull(df), None).to_dict(orient="records")
        for i in range(0, len(records), BATCH_SIZE):
            batch = records[i:i + BATCH_SIZE]
            client.table(table).upsert(batch).execute()
        print(f"seeded {table}: {len(records)} rows")


if __name__ == "__main__":
    main()
