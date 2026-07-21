/**
 * Small reusable pieces every screen needs: a loading skeleton
 * (so the UI doesn't just flash blank while fetching) and an
 * error state (so a backend outage doesn't look like a blank crash).
 */

export function LoadingSkeleton({ rows = 4 }: { rows?: number }) {
  return (
    <div className="animate-pulse space-y-3">
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="h-20 bg-card rounded-lg border border-gray-800" />
      ))}
    </div>
  );
}

export function ErrorState({
  message,
  onRetry,
}: {
  message: string;
  onRetry?: () => void;
}) {
  return (
    <div className="bg-card border border-danger/30 rounded-lg p-6 text-center">
      <p className="text-danger text-sm font-medium mb-1">Couldn&apos;t load data</p>
      <p className="text-gray-500 text-xs mb-4">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-4 py-2 text-xs rounded-md bg-accent/15 text-accent hover:bg-accent/25 transition-colors"
        >
          Try again
        </button>
      )}
    </div>
  );
}
