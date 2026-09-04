from src.generate_tickets import generate_tickets


def test_generator_creates_requested_number_of_tickets():
    tickets = generate_tickets(total=7, seed=42)
    assert len(tickets) == 7
    assert tickets[0]["ticket_id"] == "TICKET-0001"
    assert tickets[-1]["ticket_id"] == "TICKET-0007"