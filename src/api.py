import json
from pathlib import Path

from fastapi import FastAPI, HTTPException


app = FastAPI(
    title="Customer Suport Analytics API",
    description="Local API that provides fictional support tickets",
    version="1.0.0",
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TICKETS_PATH = PROJECT_ROOT / "data" / "tickets.json"

def load_tickets() -> list[dict]:
    """Read and return the tickets from the JSON."""
    if not TICKETS_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="The data was not found",
        )

    with TICKETS_PATH.open(encoding="utf-8") as file:
        return json.load(file)

@app.get("/api/v1/tickets")
def get_tickets() -> list[dict]:
    """Return all support tickets"""
    return load_tickets()