from fastapi import APIRouter, HTTPException
from app.services import impact_service

router = APIRouter(prefix="/api/impact", tags=["impact"])


@router.get("/{event_id}")
def get_impact(event_id: str):
    result = impact_service.compute_impact(event_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return result
