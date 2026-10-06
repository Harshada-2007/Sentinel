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
db.py ── Supabase (if SUPABASE_URL/KEY set) │ else local CSVs in backend/data (offline demo)
```

| Layer | Component |
|---|---|
| ML | Supplier risk (RandomForest), demand forecast (XGBoost, lag features, 14-day recursive), stockout (RandomForest) |
| Logic | Impact cascade, 5 levers (`services/levers.py`), simulator, PuLP LP optimizer |
| LLM | OpenAI if `OPENAI_API_KEY` set, else rule-based template (works offline) |

## Run

```bash
# Backend
cd backend
pip install -r requirements.txt
python data/generate_data.py
python app/ml/train_supplier_risk.py
python app/ml/train_demand_forecast.py
python app/ml/train_stockout.py
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev        # http://localhost:5173
```

Optional Supabase: run `supabase/schema.sql` in the SQL editor, copy `backend/.env.example` to `.env`, fill it in, then `python data/seed_supabase.py`.

## Demo path
Dashboard → Disruptions (create event) → Impact Analysis → Recommendations (Get Recommendations → Why this action? → Accept, visible in audit trail) → Simulator.

## Notes
- Training data is synthetic; labels are generated from feature-driven latent probabilities, so model metrics reflect that generator, not real-world accuracy.
- Lever cost/benefit coefficients in `levers.py` are transparent assumptions (e.g. $6.50/unit transfer), meant to be tuned.
- Pin `pulp==2.8.0` (PuLP 4.x changed its API).
