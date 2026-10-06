from fastapi import APIRouter
from app.db import get_store, now_iso, log_audit
from app.schemas import DisruptionEventCreate

router = APIRouter(prefix="/api/events", tags=["events"])


@router.get("")
def list_events():
    store = get_store()
    df = store.get_table("disruption_events")
    return df.sort_values("detected_date", ascending=False).to_dict(orient="records")


@router.post("")
def create_event(event: DisruptionEventCreate):
    store = get_store()
    event_id = store.next_id("disruption_events", prefix="EVT")
    row = {
        "event_id": event_id,
        "event_type": event.event_type,
        "affected_supplier_id": event.affected_supplier_id,
        "affected_region": event.affected_region,
        "detected_date": now_iso()[:10],
        "severity": event.severity,
        "predicted_delay_days": event.predicted_delay_days,
        "source": event.source,
        "description": event.description,
    }
    saved = store.insert_row("disruption_events", row)
    log_audit("create_event", "disruption_events", event_id, row)
    return saved
