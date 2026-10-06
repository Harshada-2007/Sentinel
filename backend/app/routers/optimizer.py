from fastapi import APIRouter
from app.schemas import OptimizerRequest, AcceptActionRequest
from app.services import optimizer_service
from app.db import get_store, now_iso, log_audit

router = APIRouter(prefix="/api/optimizer", tags=["optimizer"])


@router.post("/recommend")
def recommend(req: OptimizerRequest):
    plans = optimizer_service.recommend(req.event_id)
    return {"event_id": req.event_id, "plans": plans}


@router.post("/accept")
def accept_action(req: AcceptActionRequest):
    store = get_store()
    plans = optimizer_service.recommend(req.event_id)
    plan = next((p for p in plans if p["rank"] == req.action_plan_rank), None)
    row = {
        "id": store.next_id("recommendations"),
        "event_id": req.event_id,
        "best_action_plan_id": req.action_plan_rank,
        "explanation_text": plan["description"] if plan else "",
        "created_at": now_iso(),
    }
    store.insert_row("recommendations", row)
    log_audit("accept_action", "action_plan", req.event_id, {"rank": req.action_plan_rank, "plan": plan})
    return {"status": "accepted", "event_id": req.event_id, "plan": plan}
