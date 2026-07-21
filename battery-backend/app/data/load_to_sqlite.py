"""
Loads vehicles_telemetry.csv into a local SQLite database.
------------------------------------------------------------
This completes Part 2's requirement: "Save as vehicles_telemetry.csv
and load into SQLite or Supabase Postgres."

Why SQLite (not Postgres) for the hackathon: zero setup, no server to
run, no credentials to share across 3 laptops - just a single .db file
that works identically on Windows/Mac/Linux. If the team later wants
Supabase Postgres instead, swap this script's connection string only -
everything else that reads from the `telemetry` table via SQL stays same.

Run directly (after generate_data.py has created the CSV):
    python -m app.data.load_to_sqlite
"""

import sqlite3
import pandas as pd
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(CURRENT_DIR, "vehicles_telemetry.csv")
DB_PATH = os.path.join(CURRENT_DIR, "vehicles.db")


def load_csv_to_sqlite():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(
            f"{CSV_PATH} not found - run 'python -m app.data.generate_data' first."
        )

    df = pd.read_csv(CSV_PATH)

    conn = sqlite3.connect(DB_PATH)
    df.to_sql("telemetry", conn, if_exists="replace", index=False)

    # Index on vehicle_id + date since every query filters/sorts by these
    conn.execute("CREATE INDEX IF NOT EXISTS idx_vehicle_date ON telemetry (vehicle_id, date)")
    conn.commit()

    count = conn.execute("SELECT COUNT(*) FROM telemetry").fetchone()[0]
    vehicles = conn.execute("SELECT COUNT(DISTINCT vehicle_id) FROM telemetry").fetchone()[0]
    conn.close()

    print(f"Loaded {count} rows across {vehicles} vehicles into {DB_PATH}")


if __name__ == "__main__":
    load_csv_to_sqlite()