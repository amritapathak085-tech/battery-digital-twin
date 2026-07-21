"""
Vehicle & Fleet endpoints - owned by Member A.

IMPORTANT: GET /vehicles and GET /vehicles/{id} response shapes are
LOCKED to what Member C specified as compulsory for their simulation.
Do not change field names without telling the whole team first.
"""

from fastapi import APIRouter, HTTPException
from app.utils.data_access import (
    get_all_vehicle_ids, get_latest_snapshot, get_soh_trend
)
from app.utils.bhi import calculate_bhi, bhi_status, calculate_fleet_health_score
from app.models.schemas import VehicleListItem, VehicleDetail, FleetHealthScore

router = APIRouter(tags=["vehicles"])


@router.get("/vehicles", response_model=list[VehicleListItem])
def list_vehicles():
    """
    Returns:
    [
      {"vehicle_id": "EV001", "bhi": 82, "soh": 91.2, "status": "healthy",
       "soh_trend": [91.5, 91.4, ...]}
    ]
    """
    results = []
    for vehicle_id in get_all_vehicle_ids():
        snapshot = get_latest_snapshot(vehicle_id)
        if snapshot is None:
            continue
        bhi = calculate_bhi(snapshot)
        results.append({
            "vehicle_id": vehicle_id,
            "bhi": bhi,
            "soh": round(snapshot["soh"], 1),
            "status": bhi_status(bhi),
            "soh_trend": get_soh_trend(vehicle_id, last_n_days=30),
        })
    return results


@router.get("/vehicles/{vehicle_id}", response_model=VehicleDetail)
def get_vehicle_detail(vehicle_id: str):
    """
    Compulsory endpoint for Member C's simulation engine. Returns:
    {
      vehicle_id, bhi, soh, avg_temperature_c, charge_cycles_total,
      depth_of_discharge_pct, fast_charge_events_count, avg_charge_cap_pct
    }
    Plus a couple of extra fields (soc, soh_trend) for the frontend -
    these are additive only, nothing required has been removed or renamed.
    """
    snapshot = get_latest_snapshot(vehicle_id)
    if snapshot is None:
        raise HTTPException(status_code=404, detail=f"Vehicle '{vehicle_id}' not found")

    bhi = calculate_bhi(snapshot)

    return {
        "vehicle_id": vehicle_id,
        "bhi": bhi,
        "soh": round(snapshot["soh"], 1),
        "avg_temperature_c": round(snapshot["avg_temperature_c"], 1),
        "charge_cycles_total": round(snapshot["charge_cycles_total"], 1),
        "depth_of_discharge_pct": round(snapshot["depth_of_discharge_pct"], 1),
        "fast_charge_events_count": int(snapshot["fast_charge_events_count"]),
        "avg_charge_cap_pct": round(snapshot["avg_charge_cap_pct"], 1),
        "soc": round(snapshot["soc"], 1),
        "soh_trend": get_soh_trend(vehicle_id, last_n_days=30),
    }


@router.get("/fleet/health-score", response_model=FleetHealthScore)
def fleet_health_score():
    """Fleet-wide aggregate - used by the Fleet Overview screen."""
    vehicles_with_bhi = []
    for vehicle_id in get_all_vehicle_ids():
        snapshot = get_latest_snapshot(vehicle_id)
        if snapshot is None:
            continue
        bhi = calculate_bhi(snapshot)
        vehicles_with_bhi.append({"vehicle_id": vehicle_id, "bhi": bhi})

    return calculate_fleet_health_score(vehicles_with_bhi)
