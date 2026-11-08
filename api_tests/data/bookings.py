"""Fresh, fake booking data for every test."""

import random
import uuid
from datetime import date, timedelta

FIRST_NAMES = ["Ayesha", "Karim", "Nusrat", "Tanvir", "Mim", "Rahim"]


def future_date(days_ahead: int) -> str:
    return (date.today() + timedelta(days=days_ahead)).isoformat()


def new_booking(**overrides) -> dict:
    """A valid booking body; a unique last name makes it easy to find the booking again."""
    start = random.randint(30, 120)
    body = {
        "firstname": random.choice(FIRST_NAMES),
        "lastname": f"Tester-{uuid.uuid4().hex[:8]}",
        "totalprice": random.randint(100, 900),
        "depositpaid": True,
        "bookingdates": {"checkin": future_date(start), "checkout": future_date(start + 3)},
        "additionalneeds": "Breakfast",
    }
    body.update(overrides)
    return body


def without(body: dict, field: str) -> dict:
    return {k: v for k, v in body.items() if k != field}
