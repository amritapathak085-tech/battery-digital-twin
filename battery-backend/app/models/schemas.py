"""
Pydantic response models. These define the EXACT JSON shape FastAPI
returns - matches what Member C specified as compulsory.
"""

from pydantic import BaseModel
from typing import Optional


class VehicleListItem(BaseModel):
    """Shape for each item in GET /vehicles."""
    vehicle_id: str
    bhi: float
    soh: float
    status: str
    soh_trend: Optional[list] = None


class VehicleDetail(BaseModel):
    """Shape for GET /vehicles/{id} - the compulsory endpoint for Member C."""
    vehicle_id: str
    bhi: float
    soh: float
    avg_temperature_c: float
    charge_cycles_total: float
    depth_of_discharge_pct: float
    fast_charge_events_count: int
    avg_charge_cap_pct: float
    soc: Optional[float] = None
    soh_trend: Optional[list] = None


class FleetHealthScore(BaseModel):
    fleet_health_score: float
    total_vehicles: int
    healthy: int
    at_risk: int
    critical: int
