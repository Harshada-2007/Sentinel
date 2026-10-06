from fastapi import APIRouter
from app.schemas import ExplainRequest
from app.services import llm_service

router = APIRouter(prefix="/api", tags=["explanations"])


@router.post("/explain")
def explain(req: ExplainRequest):
    text = llm_service.generate_explanation(req.event_id, req.action_plan_rank)
    return {"event_id": req.event_id, "explanation": text}
