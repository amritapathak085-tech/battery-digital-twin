from fastapi import APIRouter

router = APIRouter()

@router.get("/business-impact/{vehicle_id}")
def business_impact(vehicle_id: str):
    return {
        "cost_saved_inr": 30660,
        "downtime_hours_avoided": 17.6,
        "co2_saved_kg": 50.4
    }


@router.get("/business-impact/fleet")
def fleet_business():
    return {
        "total_cost_saved_inr": 412000,
        "total_downtime_hours_avoided": 210,
        "total_co2_saved_kg": 890,
        "vehicles_analyzed": 20
    }