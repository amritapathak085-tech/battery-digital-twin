"""
Battery Health Index (BHI) Calculation
----------------------------------------
This is the SHARED scoring function. Member C's simulation engine calls
this exact same function on modified parameters to compute "after" scores -
so DO NOT change this function's signature without telling the team.

BHI is a 0-100 score combining:
    - State of Health (the biggest factor - directly from the battery)
    - Temperature stress (running hot ages batteries faster)
    - Cycle stress (high cycle count relative to expected life)
    - Depth of Discharge stress (deep discharges age batteries faster)

Weights below are a reasonable starting point for the hackathon. Member B
can later tune these using SHAP global feature importance from their model
so the score becomes model-grounded rather than a hand-picked formula -
but this version works standalone right now, no dependency on Member B.
"""

# ---- Tunable weights (must sum to 1.0) ----
# SoH is weighted heavily because it's the actual measured degradation -
# stress factors are secondary modifiers, not the primary signal.
WEIGHT_SOH = 0.70
WEIGHT_TEMP_STRESS = 0.10
WEIGHT_CYCLE_STRESS = 0.10
WEIGHT_DOD_STRESS = 0.10

# ---- Reference thresholds used to normalize each stress factor to 0-100 ----
TEMP_SAFE_MAX = 30       # C - below this, zero temp stress
TEMP_CRITICAL = 45       # C - at/above this, max temp stress
CYCLE_SAFE_MAX = 800     # cycles - below this, zero cycle stress
CYCLE_CRITICAL = 2500    # cycles - at/above this, max cycle stress
DOD_SAFE_MAX = 60        # % - below this, zero DoD stress
DOD_CRITICAL = 100       # % - at/above this, max DoD stress


def _normalize_stress(value: float, safe_max: float, critical: float) -> float:
    """
    Turns a raw value into a 0-100 'stress score' where 0 = no stress
    and 100 = maximum stress. Linear ramp between safe_max and critical.
    """
    if value <= safe_max:
        return 0.0
    if value >= critical:
        return 100.0
    return ((value - safe_max) / (critical - safe_max)) * 100.0


def calculate_bhi(vehicle_data: dict) -> float:
    """
    vehicle_data must contain:
        soh (float, 0-100)
        avg_temperature_c (float)
        charge_cycles_total (float)
        depth_of_discharge_pct (float)

    Returns: BHI score, float 0-100 (higher = healthier)
    """
    soh = vehicle_data["soh"]
    temp_stress = _normalize_stress(
        vehicle_data["avg_temperature_c"], TEMP_SAFE_MAX, TEMP_CRITICAL
    )
    cycle_stress = _normalize_stress(
        vehicle_data["charge_cycles_total"], CYCLE_SAFE_MAX, CYCLE_CRITICAL
    )
    dod_stress = _normalize_stress(
        vehicle_data["depth_of_discharge_pct"], DOD_SAFE_MAX, DOD_CRITICAL
    )

    # SoH contributes positively; stress factors subtract from the score
    score = (
        WEIGHT_SOH * soh
        + WEIGHT_TEMP_STRESS * (100 - temp_stress)
        + WEIGHT_CYCLE_STRESS * (100 - cycle_stress)
        + WEIGHT_DOD_STRESS * (100 - dod_stress)
    )
    return round(max(0, min(100, score)), 1)


def bhi_status(bhi: float) -> str:
    """Maps a BHI score to a status label used across the frontend."""
    if bhi >= 80:
        return "healthy"
    elif bhi >= 65:
        return "at_risk"
    else:
        return "critical"


def calculate_fleet_health_score(vehicles: list) -> dict:
    """
    vehicles: list of dicts, each already containing a 'bhi' key
    (call calculate_bhi() on each vehicle first, then pass the list here)
    """
    if not vehicles:
        return {
            "fleet_health_score": 0, "total_vehicles": 0,
            "healthy": 0, "at_risk": 0, "critical": 0
        }

    bhis = [v["bhi"] for v in vehicles]
    statuses = [bhi_status(b) for b in bhis]

    return {
        "fleet_health_score": round(sum(bhis) / len(bhis), 1),
        "total_vehicles": len(vehicles),
        "healthy": statuses.count("healthy"),
        "at_risk": statuses.count("at_risk"),
        "critical": statuses.count("critical"),
    }
