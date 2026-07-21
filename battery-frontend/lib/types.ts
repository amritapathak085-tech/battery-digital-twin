/**
 * Shared types - mirrors the FastAPI response shapes exactly.
 * Keep this in sync with app/models/schemas.py on the backend.
 * If Member B or C add new endpoints, add their types here too
 * so everyone gets autocomplete + type safety.
 */

export interface VehicleListItem {
  vehicle_id: string;
  bhi: number;
  soh: number;
  status: "healthy" | "at_risk" | "critical";
  soh_trend: number[];
}

export interface VehicleDetail extends VehicleListItem {
  avg_temperature_c: number;
  charge_cycles_total: number;
  depth_of_discharge_pct: number;
  fast_charge_events_count: number;
  avg_charge_cap_pct: number;
  soc: number;
}

export interface FleetHealthScore {
  fleet_health_score: number;
  total_vehicles: number;
  healthy: number;
  at_risk: number;
  critical: number;
}
