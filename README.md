# Sentinel Control Tower

AI control tower for supply chain operations: predicts disruptions, quantifies impact, simulates responses, and recommends the cheapest action across 5 levers.

## Architecture

```
React (Vite, Tailwind, React Query, Recharts)
        │  Axios (only talks to FastAPI)
        ▼
FastAPI routers ──► services ──► ML models (.pkl) + PuLP optimizer + LLM layer
        │
        ▼
db.py ── Supabase (if SUPABASE_URL/KEY set) │ else local CSVs in backend/data 
```
