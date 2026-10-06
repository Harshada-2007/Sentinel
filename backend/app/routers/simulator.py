from fastapi import APIRouter
from app.schemas import SimulatorRequest
from app.services import simulator_service

router = APIRouter(prefix="/api/simulator", tags=["simulator"])


@router.post("/run")
def run_simulator(req: SimulatorRequest):
    return simulator_service.run_simulation(req.event_id, req.actions)
