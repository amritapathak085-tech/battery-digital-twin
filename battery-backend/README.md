# Battery Digital Twin - Backend (Member A's Foundation)

## What's in here

```
battery-backend/
├── app/
│   ├── main.py              <- FastAPI app entrypoint, CORS, router registration
│   ├── config.py             <- env variable loading (shared by whole team)
│   ├── routers/
│   │   └── vehicles.py       <- GET /vehicles, GET /vehicles/{id}, GET /fleet/health-score
│   ├── models/
│   │   └── schemas.py        <- pydantic response shapes (the "contract")
│   ├── utils/
│   │   ├── bhi.py            <- calculate_bhi() - SHARED, Member C's simulation uses this too
│   │   └── data_access.py    <- CSV loading helpers
│   └── data/
│       ├── generate_data.py  <- synthetic data generator
│       └── vehicles_telemetry.csv   <- generated output (20 vehicles x 365 days)
├── requirements.txt
├── .env.example
└── README.md
```

## Setup (everyone on the team runs this once)

```bash
cd battery-backend
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # fill in GEMINI_API_KEY when you have it
```

## Regenerate the data (only if you want different numbers)

```bash
python -m app.data.generate_data
```

This overwrites `app/data/vehicles_telemetry.csv`. Random seed is fixed (42),
so everyone gets identical data unless you change the seed.

## Run the server

```bash
uvicorn app.main:app --reload --port 8000
```

Then open **http://localhost:8000/docs** for interactive Swagger docs -
you can test every endpoint from the browser without needing the frontend.

## Endpoints live right now

| Endpoint | Returns |
|---|---|
| `GET /health` | `{"status": "ok"}` |
| `GET /vehicles` | List of all vehicles with `vehicle_id`, `bhi`, `soh`, `status` |
| `GET /vehicles/{id}` | Full detail for one vehicle (compulsory shape for Member C) |
| `GET /fleet/health-score` | Fleet-wide `fleet_health_score`, `healthy`/`at_risk`/`critical` counts |

Current fleet distribution: **13 healthy, 6 at-risk, 1 critical** (out of 20 vehicles) -
this gives the Alerts screen and demo something meaningful to show.

## For Member B (Predictive Maintenance + Explainable AI)

- Read telemetry via `from app.utils.data_access import load_telemetry, get_full_history`
- Add your router at `app/routers/predictions.py` and `app/routers/copilot.py`
- Register it in `app/main.py` (see the commented-out lines already there)
- Train your models on the full `vehicles_telemetry.csv` history, not just latest snapshot

## For Member C (Simulation + Business Impact)

- **`calculate_bhi(vehicle_data: dict)` in `app/utils/bhi.py` is the exact function to reuse**
  for your simulation's "after" score - just build a modified dict and call the same function.
- `GET /vehicles/{id}` gives you the full current feature vector to start your simulation from.
- Add your router at `app/routers/simulation.py` and `app/routers/business_impact.py`
- Register it in `app/main.py` the same way.

## Status: ✅ Working and tested

All endpoints verified against the exact JSON contract. Data regenerated with a
realistic degradation spread (57%-93% SoH range) so the demo has visible variety
across healthy/at-risk/critical vehicles instead of everything looking the same.
