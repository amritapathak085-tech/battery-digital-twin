/**
 * Shared API fetch wrapper.
 * ---------------------------------------------------------------
 * Every teammate's component should call `apiGet` / `apiPost` from
 * here instead of using fetch() directly - this way error handling,
 * the base URL, and JSON parsing all stay consistent across the app.
 *
 * Set NEXT_PUBLIC_API_URL in .env.local, e.g.:
 *   NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
 */

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export class ApiError extends Error {
  status?: number;
  constructor(message: string, status?: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

/**
 * GET request helper.
 * Usage: const vehicles = await apiGet<VehicleListItem[]>("/vehicles");
 */
export async function apiGet<T>(path: string): Promise<T> {
  try {
    const res = await fetch(`${BASE_URL}${path}`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      cache: "no-store",
    });

    if (!res.ok) {
      throw new ApiError(`Request failed: ${res.status} ${res.statusText}`, res.status);
    }

    return (await res.json()) as T;
  } catch (err) {
    // Re-throw as ApiError so every caller can handle failures the same way,
    // whether it's a network error, a timeout, or a bad response from the API.
    if (err instanceof ApiError) throw err;
    throw new ApiError(
      err instanceof Error ? err.message : "Network error - is the backend running?"
    );
  }
}

/**
 * POST request helper.
 * Usage: const result = await apiPost<SimResult>("/vehicles/EV001/simulate", { changed_params: {...} });
 */
export async function apiPost<T>(path: string, body: unknown): Promise<T> {
  try {
    const res = await fetch(`${BASE_URL}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      throw new ApiError(`Request failed: ${res.status} ${res.statusText}`, res.status);
    }

    return (await res.json()) as T;
  } catch (err) {
    if (err instanceof ApiError) throw err;
    throw new ApiError(
      err instanceof Error ? err.message : "Network error - is the backend running?"
    );
  }
}
