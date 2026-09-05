"""Fetch fictional support tickets from the local API."""

import requests


API_URL = "http://127.0.0.1:8000/api/v1/tickets"

def fetch_tickets() -> list[dict]:
    """Request all tickets from the API"""
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()

    return response.json()

if __name__ == "__main__":
    tickets = fetch_tickets()
    print(f"Received {len(tickets)} tickets from the API")
    print(f"First ticket ID: {tickets[0]['ticket_id']}")