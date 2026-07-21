"use client";

import { useEffect, useState, useCallback } from "react";
import {
  RadialBarChart,
  RadialBar,
  PolarAngleAxis,
  LineChart,
  Line,
  ResponsiveContainer,
} from "recharts";
import { apiGet } from "@/lib/api";
import type { VehicleListItem, FleetHealthScore } from "@/lib/types";
import StatusBadge from "@/components/StatusBadge";
import { LoadingSkeleton, ErrorState } from "@/components/LoadingAndError";

// Picks a gauge color based on score - mirrors the same thresholds as
// bhi_status() on the backend (healthy >=80, at_risk >=65, else critical)
function gaugeColor(score: number) {
  if (score >= 80) return "#22c55e"; // success
  if (score >= 65) return "#eab308"; // warning
  return "#ef4444"; // danger
}

export default function FleetOverview() {
  const [vehicles, setVehicles] = useState<VehicleListItem[] | null>(null);
  const [fleetScore, setFleetScore] = useState<FleetHealthScore | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const loadData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      // Fetch both endpoints in parallel - no reason to wait sequentially
      const [vehicleList, healthScore] = await Promise.all([
        apiGet<VehicleListItem[]>("/vehicles"),
        apiGet<FleetHealthScore>("/fleet/health-score"),
      ]);
      setVehicles(vehicleList);
      setFleetScore(healthScore);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  if (loading) {
    return (
      <div>
        <h1 className="text-xl font-semibold text-gray-100 mb-6">Fleet Overview</h1>
        <LoadingSkeleton rows={5} />
      </div>
    );
  }

  if (error || !vehicles || !fleetScore) {
    return (
      <div>
        <h1 className="text-xl font-semibold text-gray-100 mb-6">Fleet Overview</h1>
        <ErrorState
          message={error || "No data returned from the API"}
          onRetry={loadData}
        />
      </div>
    );
  }

  const gaugeData = [
    { value: fleetScore.fleet_health_score, fill: gaugeColor(fleetScore.fleet_health_score) },
  ];

  return (
    <div>
      <h1 className="text-xl font-semibold text-gray-100 mb-6">Fleet Overview</h1>

      {/* --- Fleet Health Score card with radial gauge --- */}
      <div className="bg-card border border-gray-800 rounded-xl p-6 mb-8 flex items-center gap-8">
        <div className="w-40 h-40 relative shrink-0">
          <ResponsiveContainer width="100%" height="100%">
            <RadialBarChart
              innerRadius="75%"
              outerRadius="100%"
              data={gaugeData}
              startAngle={90}
              endAngle={-270}
            >
              <PolarAngleAxis type="number" domain={[0, 100]} angleAxisId={0} tick={false} />
              <RadialBar background dataKey="value" cornerRadius={8} />
            </RadialBarChart>
          </ResponsiveContainer>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="font-data text-3xl font-bold text-gray-100">
              {fleetScore.fleet_health_score}
            </span>
            <span className="text-xs text-gray-500">/ 100</span>
          </div>
        </div>

        <div>
          <p className="text-sm text-gray-400 mb-3">Fleet Health Score</p>
          <div className="flex gap-6 font-data text-sm">
            <div>
              <span className="text-success font-semibold">{fleetScore.healthy}</span>
              <span className="text-gray-500 ml-1.5">Healthy</span>
            </div>
            <div>
              <span className="text-warning font-semibold">{fleetScore.at_risk}</span>
              <span className="text-gray-500 ml-1.5">At Risk</span>
            </div>
            <div>
              <span className="text-danger font-semibold">{fleetScore.critical}</span>
              <span className="text-gray-500 ml-1.5">Critical</span>
            </div>
          </div>
          <p className="text-xs text-gray-600 mt-3">
            {fleetScore.total_vehicles} vehicles monitored
          </p>
        </div>
      </div>

      {/* --- Vehicle card grid --- */}
      <p className="text-sm text-gray-500 mb-3">All Vehicles</p>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {vehicles.map((vehicle) => (
          <div
            key={vehicle.vehicle_id}
            className="bg-card border border-gray-800 rounded-lg p-4 hover:border-gray-700 transition-colors"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="font-data text-sm font-semibold text-gray-100">
                {vehicle.vehicle_id}
              </span>
              <StatusBadge status={vehicle.status} />
            </div>

            <div className="flex items-end justify-between">
              <div>
                <p className="font-data text-2xl font-bold text-gray-100">{vehicle.bhi}</p>
                <p className="text-xs text-gray-500">BHI Score</p>
              </div>

              {/* Mini sparkline of SoH trend - minimal style, no axes */}
              <div className="w-20 h-10">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={vehicle.soh_trend.map((v, i) => ({ i, v }))}>
                    <Line
                      type="monotone"
                      dataKey="v"
                      stroke={gaugeColor(vehicle.bhi)}
                      strokeWidth={2}
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
