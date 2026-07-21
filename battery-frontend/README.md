# Battery Digital Twin - Frontend (Member A's Foundation)

## What's in here

```
battery-frontend/
├── app/
│   ├── layout.tsx           <- root shell with sidebar (shared by whole team)
│   ├── page.tsx              <- Fleet Overview (home route "/")
│   ├── globals.css           <- theme colors, fonts (Inter + JetBrains Mono)
│   ├── alerts/page.tsx        <- Alerts screen
│   ├── predictions/page.tsx   <- placeholder for Member B
│   ├── simulation/page.tsx    <- placeholder for Member C
│   └── reports/page.tsx       <- placeholder for Member C
├── components/
│   ├── Sidebar.tsx            <- nav shell, route-based highlighting
│   ├── FleetOverview.tsx      <- Screen 1: gauge + vehicle card grid
│   ├── Alerts.tsx             <- Screen 2: risk-sorted table
│   ├── StatusBadge.tsx        <- shared healthy/at_risk/critical pill
│   └── LoadingAndError.tsx    <- shared skeleton + error state
├── lib/
│   ├── api.ts                 <- shared fetch wrapper (apiGet/apiPost)
│   └── types.ts                <- shared TypeScript types matching backend
├── tailwind.config.js          <- exact color palette from the spec
└── package.json
```

## Setup

```bash
cd battery-frontend
npm install
cp .env.local.example .env.local
```

Edit `.env.local` if your backend runs somewhere other than
`http://127.0.0.1:8000`.

## Run it

Make sure the backend (`battery-backend`) is running first on port 8000,
then in a separate terminal:

```bash
npm run dev
```

Open **http://localhost:3000** - you should see the Fleet Overview screen
with the radial gauge and vehicle cards populated from real backend data.

## Verified working

- ✅ TypeScript compiles with zero errors (`npx tsc --noEmit`)
- ✅ Production build succeeds (`npm run build`)
- ✅ CORS confirmed working between frontend (port 3000) and backend (port 8000)
- ✅ All 6 routes render: `/`, `/alerts`, `/predictions`, `/simulation`, `/reports`

## For Member B (Predictions screen)

Open `app/predictions/page.tsx` - it already reads the `?vehicle=EV001` query
param passed from the Alerts screen's "View Details" button. Build your
screen inside `PredictionsContent()`, keeping the `<Suspense>` wrapper
(Next.js 14 requires this for `useSearchParams()` or the production build
fails - I already hit this error and fixed it, so you don't have to).

Use `apiGet<T>("/vehicles/{id}/prediction")` from `lib/api.ts` - same
pattern as FleetOverview.tsx and Alerts.tsx.

## For Member C (Simulation + Reports screens)

Same pattern - build inside `app/simulation/page.tsx` and `app/reports/page.tsx`.
Use `apiPost<T>("/vehicles/{id}/simulate", body)` for the simulation call.
Add any new response types to `lib/types.ts` so everyone gets autocomplete.

## Design tokens (do not hardcode hex values elsewhere)

All colors are defined once in `tailwind.config.js`:
- `bg-background` `#0a0e14` | `bg-card` `#131822` | `text-accent` `#3b82f6`
- `text-success` `#22c55e` | `text-warning` `#eab308` | `text-danger` `#ef4444`

Use `font-data` class (JetBrains Mono) on any element showing a number.
