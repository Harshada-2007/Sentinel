from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class SupplierOut(BaseModel):
    supplier_id: str
    name: str
    tier: int
    location: str
    lead_time_days: int
    unit_cost: float
    capacity_units: int
    reliability_score: float
    backup_for: Optional[str] = None
    risk_score: Optional[float] = None


class SupplierRiskOut(BaseModel):
    supplier_id: str
    delay_probability: float
    risk_tier: str
    explanation: str
    top_factors: List[Dict[str, Any]]


class InventoryOut(BaseModel):
    inventory_id: str
    product_id: str
    warehouse_id: str
    quantity_on_hand: int
    quantity_in_transit: int
    last_updated: str


class StockoutRiskOut(BaseModel):
    product_id: str
    warehouse_id: str
    stockout_probability: float
    days_to_stockout: Optional[float] = None


class OrderOut(BaseModel):
    order_id: str
    product_id: str
    warehouse_id: str
    customer_id: str
    customer_tier: str
    quantity: int
    order_date: str
    promised_delivery_date: str
    priority_score: float
    status: str


class DisruptionEventOut(BaseModel):
    event_id: str
    event_type: str
    affected_supplier_id: str
    affected_region: str
    detected_date: str
    severity: float
    predicted_delay_days: int
    source: str
    description: str


class DisruptionEventCreate(BaseModel):
    event_type: str
    affected_supplier_id: str
    affected_region: str
    severity: float
    predicted_delay_days: int
    source: str = "manual_entry"
    description: str


class DemandForecastOut(BaseModel):
    product_id: str
    forecast: List[Dict[str, Any]]


class ImpactOut(BaseModel):
    event_id: str
    affected_supplier: Dict[str, Any]
    affected_products: List[Dict[str, Any]]
    affected_orders_count: int
    revenue_at_risk: float
    cascade: Dict[str, Any]


class SimulatorAction(BaseModel):
    lever: int
    params: Dict[str, Any] = {}


class SimulatorRequest(BaseModel):
    event_id: str
    actions: List[SimulatorAction]


class SimulatorOutcome(BaseModel):
    stockout_risk_pct: float
    sla_pct: float
    total_cost: float
    details: List[Dict[str, Any]]


class SimulatorResponse(BaseModel):
    event_id: str
    do_nothing: SimulatorOutcome
    with_actions: SimulatorOutcome


class OptimizerRequest(BaseModel):
    event_id: str


class ActionPlanOut(BaseModel):
    rank: int
    levers_used: List[int]
    description: str
    estimated_cost: float
    expected_stockout_reduction: float
    sla_impact: float
    feasibility: float


class OptimizerResponse(BaseModel):
    event_id: str
    plans: List[ActionPlanOut]


class ExplainRequest(BaseModel):
    event_id: str
    action_plan_rank: int = 1


class ExplainResponse(BaseModel):
    event_id: str
    explanation: str


class AcceptActionRequest(BaseModel):
    event_id: str
    action_plan_rank: int


class KpiOut(BaseModel):
    suppliers_at_risk: int
    dollar_exposure: float
    stockouts_predicted: int
    active_events: int
