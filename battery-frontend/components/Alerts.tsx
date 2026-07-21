"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { apiGet } from "@/lib/api";
import type { VehicleListItem } from "@/lib/types";
import StatusBadge from "@/components/StatusBadge";
import { LoadingSkeleton, ErrorState } from "@/components/LoadingAndError";

export default function Alerts() {
  const router = useRouter();
  const [vehicles, setVehicles] = useState<VehicleListItem[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const loadData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiGet<VehicleListItem[]>("/vehicles");
      // Sort lowest BHI first - the riskiest vehicles need attention first
      const sorted = [...data].sort((a, b) => a.bhi - b.bhi);
      setVehicles(sorted);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  // Member B builds the actual /predictions screen - this just wires
  // the navigation with the vehicle pre-selected via a query param.
  function goToPredictions(vehicleId: string) {
    router.push(`/predictions?vehicle=${vehicleId}`);
  }

  if (loading) {
    return (
      <div>
        <h1 className="text-xl font-semibold text-gray-100 mb-6">Alerts</h1>
        <LoadingSkeleton rows={6} />
      </div>
    );
  }

  if (error || !vehicles) {
    return (
      <div>
        <h1 className="text-xl font-semibold text-gray-100 mb-6">Alerts</h1>
        <ErrorState message={error || "No data returned from the API"} onRetry={loadData} />
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-xl font-semibold text-gray-100 mb-2">Alerts</h1>
      <p className="text-sm text-gray-500 mb-6">
        Vehicles ranked by risk - lowest health score first
      </p>

      <div className="bg-card border border-gray-800 rounded-xl overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-800 text-left text-gray-500 text-xs uppercase tracking-wide">
              <th className="px-5 py-3 font-medium">Vehicle ID</th>
              <th className="px-5 py-3 font-medium">BHI</th>
              <th className="px-5 py-3 font-medium">Status</th>
              <th className="px-5 py-3 font-medium text-right">Action</th>
            </tr>
          </thead>
          <tbody>
            {vehicles.map((vehicle) => (
              <tr
                key={vehicle.vehicle_id}
                className="border-b border-gray-800/60 last:border-0 hover:bg-white/[0.02] transition-colors"
              >
                <td className="px-5 py-4 font-data font-medium text-gray-100">
                  {vehicle.vehicle_id}
                </td>
                <td className="px-5 py-4 font-data text-gray-300">{vehicle.bhi}</td>
                <td className="px-5 py-4">
                  <StatusBadge status={vehicle.status} />
                </td>
                <td className="px-5 py-4 text-right">
                  <button
                    onClick={() => goToPredictions(vehicle.vehicle_id)}
                    className="px-3 py-1.5 text-xs rounded-md bg-accent/15 text-accent hover:bg-accent/25 transition-colors"
                  >
                    View Details
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
