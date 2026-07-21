/**
 * StatusBadge - color-coded pill used anywhere a vehicle's health
 * status needs to show up (Fleet Overview cards, Alerts table, etc).
 *
 * Color mapping matches the spec exactly:
 *   healthy (BHI > 70) -> green
 *   at_risk (BHI 40-70) -> yellow
 *   critical (BHI < 40) -> red
 */

type Status = "healthy" | "at_risk" | "critical";

const STATUS_CONFIG: Record<Status, { label: string; classes: string }> = {
  healthy: {
    label: "Healthy",
    classes: "bg-success/15 text-success border border-success/30",
  },
  at_risk: {
    label: "At Risk",
    classes: "bg-warning/15 text-warning border border-warning/30",
  },
  critical: {
    label: "Critical",
    classes: "bg-danger/15 text-danger border border-danger/30",
  },
};

export default function StatusBadge({ status }: { status: Status }) {
  const config = STATUS_CONFIG[status] ?? STATUS_CONFIG.at_risk;
  return (
    <span
      className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium ${config.classes}`}
    >
      {config.label}
    </span>
  );
}
