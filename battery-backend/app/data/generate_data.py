"""
Synthetic EV Fleet Battery Telemetry Generator
------------------------------------------------
Generates 12 months of daily telemetry for 20 vehicles.

Columns (matches what Member C asked for exactly):
    vehicle_id, soh, soc, avg_temperature_c, charge_cycles_total,
    depth_of_discharge_pct, fast_charge_events_count, avg_charge_cap_pct

We also keep a `date` column so the frontend can draw SoH trend
sparklines - this doesn't remove or rename anything Member C needs,
it's an extra column they can just ignore if unused.

Run directly:  python -m app.data.generate_data
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

# Reproducible randomness so everyone on the team gets the same demo data
np.random.seed(42)

NUM_VEHICLES = 20
DAYS = 365
START_DATE = datetime(2025, 7, 1)


def generate_vehicle_profile(vehicle_index: int) -> dict:
    """
    Give each vehicle a distinct 'usage personality' so the fleet isn't
    uniform - some vehicles run hot, some fast-charge a lot, etc.
    This is what makes the BHI/alerts screen look realistic in the demo:
    roughly a third healthy, a third at-risk, a third critical after a year.
    """
    rng = np.random.default_rng(seed=vehicle_index)
    return {
        "base_temp": rng.uniform(22, 34),           # baseline operating temp (C)
        "temp_volatility": rng.uniform(2, 9),         # how much temp swings day to day
        "daily_cycle_rate": rng.uniform(1.0, 3.5),    # charge cycles added per day (industrial usage)
        "dod_tendency": rng.uniform(40, 90),          # typical depth of discharge %
        "fast_charge_habit": rng.uniform(0, 4),       # avg fast-charge events/day
        "charge_cap_habit": rng.uniform(70, 100),     # typical charge cap %
        # Baseline % SoH lost per 100 cycles under NO stress - varies per vehicle
        # so identical usage patterns still age differently (manufacturing variance)
        "base_loss_per_100_cycles": rng.uniform(0.35, 2.2),
    }


def simulate_vehicle(vehicle_index: int) -> pd.DataFrame:
    vehicle_id = f"EV{str(vehicle_index + 1).zfill(3)}"
    profile = generate_vehicle_profile(vehicle_index)
    rng = np.random.default_rng(seed=1000 + vehicle_index)

    records = []
    soh = 100.0  # every battery starts at 100% health

    for day in range(DAYS):
        date = START_DATE + timedelta(days=day)

        # --- Daily operating conditions (with noise) ---
        avg_temperature_c = max(
            10, profile["base_temp"] + rng.normal(0, profile["temp_volatility"])
        )
        depth_of_discharge_pct = float(
            np.clip(profile["dod_tendency"] + rng.normal(0, 8), 15, 100)
        )
        fast_charge_events_count = max(
            0, int(round(profile["fast_charge_habit"] + rng.normal(0, 1)))
        )
        avg_charge_cap_pct = float(
            np.clip(profile["charge_cap_habit"] + rng.normal(0, 3), 60, 100)
        )
        soc = float(np.clip(rng.uniform(20, avg_charge_cap_pct), 10, 100))

        cycles_today = profile["daily_cycle_rate"] * rng.uniform(0.7, 1.3)
        charge_cycles_total = round(
            (records[-1]["charge_cycles_total"] if records else 0) + cycles_today, 2
        )

        # --- Degradation logic (this is the physics-ish part) ---
        # Base degradation varies per vehicle (manufacturing variance)
        base_loss = (cycles_today / 100) * profile["base_loss_per_100_cycles"]

        # Stress multipliers - each condition compounds the degradation
        stress_multiplier = 1.0
        if avg_temperature_c > 35:
            stress_multiplier += 0.9
        if depth_of_discharge_pct > 80:
            stress_multiplier += 0.6
        if fast_charge_events_count >= 2:
            stress_multiplier += 0.5
        if avg_charge_cap_pct > 90:
            stress_multiplier += 0.4
        stress_multiplier = min(stress_multiplier, 3.5)  # cap so it doesn't run away

        daily_loss = base_loss * stress_multiplier
        daily_loss += rng.normal(0, 0.003)  # tiny random noise
        daily_loss = max(daily_loss, 0)

        soh = max(soh - daily_loss, 55)  # floor so it doesn't go negative

        records.append({
            "vehicle_id": vehicle_id,
            "date": date.strftime("%Y-%m-%d"),
            "soh": round(soh, 2),
            "soc": round(soc, 2),
            "avg_temperature_c": round(avg_temperature_c, 2),
            "charge_cycles_total": charge_cycles_total,
            "depth_of_discharge_pct": round(depth_of_discharge_pct, 2),
            "fast_charge_events_count": fast_charge_events_count,
            "avg_charge_cap_pct": round(avg_charge_cap_pct, 2),
        })

    return pd.DataFrame(records)


def generate_fleet_data() -> pd.DataFrame:
    all_dfs = [simulate_vehicle(i) for i in range(NUM_VEHICLES)]
    return pd.concat(all_dfs, ignore_index=True)


def main():
    df = generate_fleet_data()
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vehicles_telemetry.csv")
    df.to_csv(out_path, index=False)
    print(f"Generated {len(df)} rows for {NUM_VEHICLES} vehicles -> {out_path}")
    print(df.groupby("vehicle_id")["soh"].last().sort_values().to_string())


if __name__ == "__main__":
    main()
