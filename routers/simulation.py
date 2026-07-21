from fastapi import APIRouter

router = APIRouter()

@router.post("/vehicles/{vehicle_id}/simulate")
def simulate(vehicle_id: str):
    return {
        "vehicle_id": vehicle_id,
        "status": "Simulation API Working 🚀"
    }