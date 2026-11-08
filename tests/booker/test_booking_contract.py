"""Contract checks: typed models (pydantic) and JSON schemas (jsonschema) must both accept the responses."""

import pytest

from api_tests.contracts import schema_errors
from api_tests.data.bookings import new_booking
from api_tests.models.booking import Booking, BookingId, CreatedBooking

pytestmark = [pytest.mark.booker, pytest.mark.contract]


def test_created_booking_follows_the_contract(bookings, authorized_bookings):
    body = bookings.create(new_booking()).json()
    try:
        assert schema_errors(body, "created_booking.schema.json") == []
        CreatedBooking.model_validate(body)
    finally:
        authorized_bookings.delete(body["bookingid"])


def test_single_booking_follows_the_contract(bookings, created_booking):
    body = bookings.get(created_booking["bookingid"]).json()
    assert schema_errors(body, "booking.schema.json") == []
    booking = Booking.model_validate(body)
    assert booking.bookingdates.checkout > booking.bookingdates.checkin


def test_booking_id_list_follows_the_contract(bookings):
    body = bookings.list_ids().json()
    assert schema_errors(body, "booking_ids.schema.json") == []
    assert [BookingId.model_validate(item) for item in body[:20]]


def test_booking_response_has_json_headers(bookings, created_booking):
    response = bookings.get(created_booking["bookingid"])
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"
    assert "ETag" in response.headers


def test_schema_rejects_a_wrong_type():
    """Guards the contract itself: a broken body must produce errors."""
    broken = {**new_booking(), "totalprice": "250", "extra": True}
    errors = schema_errors(broken, "booking.schema.json")
    assert any("totalprice" in e for e in errors)
    assert any("extra" in e for e in errors)
