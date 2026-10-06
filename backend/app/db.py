"""
db.py — Unified data access layer.

If SUPABASE_URL / SUPABASE_KEY are set (see config.py), all reads/writes go
through the Supabase Python client against the tables defined in
supabase/schema.sql. Otherwise the app falls back to the local CSVs in
backend/data/ (produced by data/generate_data.py) plus an in-memory audit
log / event-creation buffer, so the whole system is runnable and demoable
with zero external services.

Every router/service in this app only talks to this module — never to
Supabase or pandas directly — so swapping the backing store is a one-file
change.
"""
import os
import threading
from datetime import datetime, timezone

import pandas as pd

from app.config import USE_SUPABASE, SUPABASE_URL, SUPABASE_KEY, DATA_DIR

_lock = threading.Lock()

TABLE_FILES = {
    "suppliers": "suppliers.csv",
    "products": "products.csv",
    "warehouses": "warehouses.csv",
    "inventory": "inventory.csv",
    "orders": "orders.csv",
    "disruption_events": "disruption_events.csv",
    "demand_history": "demand_history.csv",
}

# tables that only exist as runtime-generated records (not seeded from CSV)
_RUNTIME_TABLES = ["action_plans", "recommendations", "audit_log"]


class LocalStore:
    """In-memory + CSV-backed store used when Supabase isn't configured."""

    def __init__(self):
        self._tables = {}
        for name, fname in TABLE_FILES.items():
            path = os.path.join(DATA_DIR, fname)
            self._tables[name] = pd.read_csv(path) if os.path.exists(path) else pd.DataFrame()
        for name in _RUNTIME_TABLES:
            self._tables[name] = pd.DataFrame()
        self._next_id = {"disruption_events": len(self._tables["disruption_events"]) + 1,
                          "action_plans": 1, "recommendations": 1, "audit_log": 1}

    def get_table(self, name: str) -> pd.DataFrame:
        return self._tables.get(name, pd.DataFrame()).copy()

    def insert_row(self, name: str, row: dict) -> dict:
        with _lock:
            df = self._tables.get(name, pd.DataFrame())
            new_row = pd.DataFrame([row])
            self._tables[name] = pd.concat([df, new_row], ignore_index=True)
            return row

    def next_id(self, table: str, prefix: str = "") -> str:
        with _lock:
            n = self._next_id.get(table, 1)
            self._next_id[table] = n + 1
            return f"{prefix}{n:05d}" if prefix else n


class SupabaseStore:
    """Thin wrapper over the Supabase Python client."""

    def __init__(self, url: str, key: str):
        from supabase import create_client
        self.client = create_client(url, key)

    def get_table(self, name: str) -> pd.DataFrame:
        resp = self.client.table(name).select("*").execute()
        return pd.DataFrame(resp.data)

    def insert_row(self, name: str, row: dict) -> dict:
        resp = self.client.table(name).insert(row).execute()
        return resp.data[0] if resp.data else row

    def next_id(self, table: str, prefix: str = "") -> str:
        # Supabase tables use serial/uuid PKs generated server-side; caller
        # should omit the id field and let Postgres assign it. Kept here
        # only so callers have a single interface across both backends.
        import uuid
        return f"{prefix}{uuid.uuid4().hex[:8]}"


_store = None


def get_store():
    global _store
    if _store is None:
        if USE_SUPABASE:
            _store = SupabaseStore(SUPABASE_URL, SUPABASE_KEY)
        else:
            _store = LocalStore()
    return _store


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def log_audit(user_action: str, entity: str, entity_id: str, payload: dict):
    store = get_store()
    store.insert_row("audit_log", {
        "id": store.next_id("audit_log"),
        "user_action": user_action,
        "entity": entity,
        "entity_id": entity_id,
        "timestamp": now_iso(),
        "payload": payload,
    })
