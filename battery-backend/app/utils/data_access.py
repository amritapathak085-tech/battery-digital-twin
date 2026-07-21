"""
Shared data-loading helper. Every router (yours, Member B's, Member C's)
should read vehicle data through these functions instead of re-reading
the CSV directly - keeps one source of truth and makes it trivial to
swap CSV for a real database later without touching router code.
"""

import pandas as pd
from app.config import settings

_df_cache = None  # simple in-memory cache so we don't re-read the CSV on every request


def load_telemetry() -> pd.DataFrame:
    global _df_cache
    if _df_cache is None:
        _df_cache = pd.read_csv(settings.TELEMETRY_CSV_PATH)
    return _df_cache


def get_all_vehicle_ids() -> list:
    df = load_telemetry()
    return sorted(df["vehicle_id"].unique().tolist())


def get_latest_snapshot(vehicle_id: str) -> dict | None:
    """Returns the most recent day's telemetry row for one vehicle as a dict."""
    df = load_telemetry()
    vehicle_rows = df[df["vehicle_id"] == vehicle_id]
    if vehicle_rows.empty:
        return None
    latest = vehicle_rows.sort_values("date").iloc[-1]
    return latest.to_dict()


def get_soh_trend(vehicle_id: str, last_n_days: int = 30) -> list:
    """Returns a list of recent SoH values - used for the sparkline chart."""
    df = load_telemetry()
    vehicle_rows = df[df["vehicle_id"] == vehicle_id].sort_values("date")
    return vehicle_rows["soh"].tail(last_n_days).round(2).tolist()


def get_full_history(vehicle_id: str) -> pd.DataFrame:
    df = load_telemetry()
    return df[df["vehicle_id"] == vehicle_id].sort_values("date")
