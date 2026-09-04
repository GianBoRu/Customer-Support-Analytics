"""Generate reproducible fictional customer-support tickets."""

import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "data" / "tickets.json"

TOTAL_TICKETS = 350
RANDOM_SEED = 42

CHANNELS = ["email", "chat", "web_form"]

SCENARIOS = [
    {
        "reason": "payment_issue",
        "priority": "high",
        "subject": "Payment failed",
        "message": "My card was charged, but my subscription is still inactive.",
    },
    {
        "reason": "password_reset",
        "priority": "medium",
        "subject": "Password reset",
        "message": "I did not receive the password reset email.",
    },
    {
        "reason": "invoice_request",
        "priority": "low",
        "subject": "Invoice request",
        "message": "Could you send me an invoice for my last payment?",
    },
    {
        "reason": "login_error",
        "priority": "high",
        "subject": "Login error E401",
        "message": "I receive error E401 every time I try to sign in.",
    },
    {
        "reason": "cancellation",
        "priority": "medium",
        "subject": "Account cancellation",
        "message": "I would like to cancel my account at the end of the month.",
    },
    {
        "reason": "feature_issue",
        "priority": "high",
        "subject": "Feature unavailable",
        "message": "The export button does not work in my dashboard.",
    },
    {
        "reason": "plan_information",
        "priority": "low",
        "subject": "Plan information",
        "message": "What is included in the Professional plan?",
    },
    {
        "reason": "duplicate_charge",
        "priority": "high",
        "subject": "Duplicate charge",
        "message": "I think I was charged twice for the same subscription.",
    },
    {
        "reason": "integration_error",
        "priority": "high",
        "subject": "Integration error E503",
        "message": "Our integration returns error E503 when we send data.",
    },
    {
        "reason": "account_update",
        "priority": "low",
        "subject": "Update contact details",
        "message": "I need to change the email address linked to my account.",
    },
]


def generate_tickets(total: int, seed: int) -> list[dict]:
    """Create a chosen number of structured fictional tickets."""
    random_generator = random.Random(seed)
    start_time = datetime(2026, 1, 1, 9, 0, tzinfo=timezone.utc)
    tickets = []

    for index in range(total):
        scenario = random_generator.choice(SCENARIOS)
        created_at = start_time + timedelta(
            minutes=random_generator.randint(0, 60 * 24 * 90)
        )
        first_response_at = created_at + timedelta(
            minutes=random_generator.randint(15, 480)
        )
        resolved_at = first_response_at + timedelta(
            minutes=random_generator.randint(60, 60 * 48)
        )

        ticket = {
            "ticket_id": f"TICKET-{index + 1:04d}",
            "customer_id": f"CUST-{random_generator.randint(1001, 1110)}",
            "created_at": created_at.isoformat(),
            "first_response_at": first_response_at.isoformat(),
            "resolved_at": resolved_at.isoformat(),
            "status": "resolved",
            "channel": random_generator.choice(CHANNELS),
            "priority": scenario["priority"],
            "subject": scenario["subject"],
            "message": scenario["message"],
        }

        tickets.append(ticket)

    return tickets


def save_tickets(tickets: list[dict]) -> None:
    """Save safely: replace the official file only after writing succeeds."""
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    temporary_path = OUTPUT_PATH.with_suffix(".tmp")

    with temporary_path.open("w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=2, ensure_ascii=False)

    temporary_path.replace(OUTPUT_PATH)
    print(f"{len(tickets)} tickets saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    tickets = generate_tickets(TOTAL_TICKETS, RANDOM_SEED)
    save_tickets(tickets)