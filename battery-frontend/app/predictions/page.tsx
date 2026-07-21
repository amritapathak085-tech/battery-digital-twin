"use client";

import { Suspense } from "react";
import { useSearchParams } from "next/navigation";

/**
 * PLACEHOLDER - Member B builds the real screen here.
 * The vehicle ID selected from the Alerts screen arrives via the
 * ?vehicle= query param, already wired up - just read it with
 * useSearchParams() like below and fetch GET /vehicles/{id}/prediction.
 *
 * NOTE: useSearchParams() requires a <Suspense> boundary in Next.js 14
 * App Router, or the production build fails - that's why this is split
 * into two components below. Keep this pattern when you build it out.
 */
function PredictionsContent() {
  const searchParams = useSearchParams();
  const vehicleId = searchParams.get("vehicle");

  return (
    <div>
      <h1 className="text-xl font-semibold text-gray-100 mb-2">Predictions</h1>
      <p className="text-sm text-gray-500 mb-6">
        Member B&apos;s screen goes here - RUL, Failure Probability, SHAP explanation, AI Copilot.
      </p>
      <div className="bg-card border border-gray-800 rounded-xl p-6">
        <p className="text-sm text-gray-400">
          Selected vehicle:{" "}
          <span className="font-data text-accent">{vehicleId || "none selected"}</span>
        </p>
      </div>
    </div>
  );
}

export default function PredictionsPage() {
  return (
    <Suspense fallback={<div className="text-sm text-gray-500">Loading...</div>}>
      <PredictionsContent />
    </Suspense>
  );
}
