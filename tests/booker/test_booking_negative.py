"""Missing or invalid authorisation, unknown IDs, malformed input and validation boundaries."""

import pytest

from api_tests.data.bookings import new_booking, without
from tests.conftest import known_issue

pytestmark = [pytest.mark.booker, pytest.mark.negative]

NO_AUTH = {"Accept": "application/json"}
BAD_TOKEN = {"Accept": "application/json", "Cookie": "token=invalid123"}


@pytest.mark.parametrize("headers", [NO_AUTH, BAD_TOKEN], ids=["no token", "invalid token"])
def test_should_refuse_update_without_valid_token(booker_session, created_booking, headers):
    url = f"/booking/{created_booking['bookingid']}"
    response = booker_session.put(url, json=new_booking(), headers=headers)
    assert (response.status_code, response.text) == (403, "Forbidden")


def test_should_refuse_patch_without_token(bookings, created_booking):
    response = bookings.partial_update(created_booking["bookingid"], {"firstname": "Hacker"}, NO_AUTH)
    assert response.status_code == 403


def test_should_refuse_delete_without_token(bookings, created_booking):
    assert bookings.delete(created_booking["bookingid"], NO_AUTH).status_code == 403
    assert bookings.get(created_booking["bookingid"]).status_code == 200


@pytest.mark.parametrize("booking_id", [999_999_999, "abc", -1], ids=["unknown", "text", "negative"])
def test_should_return_404_for_bookings_that_do_not_exist(bookings, booking_id):
    assert bookings.get(booking_id).status_code == 404


def test_should_reject_malformed_json(bookings):
    assert bookings.create('{"firstname": ').status_code == 400


@pytest.mark.parametrize("price", [0, 1, 99_999], ids=["zero", "one", "large"])
def test_should_accept_boundary_prices(bookings, authorized_bookings, price):
    response = bookings.create(new_booking(totalprice=price))
    assert response.status_code == 200
    assert response.json()["booking"]["totalprice"] == price
    authorized_bookings.delete(response.json()["bookingid"])


@known_issue("F-05", "missing required field returns 500 instead of 400")
def test_should_answer_400_when_firstname_is_missing(bookings):
    assert bookings.create(without(new_booking(), "firstname")).status_code == 400


@known_issue("F-06", "text price is stored as null")
def test_should_reject_price_as_text(bookings):
    assert bookings.create(new_booking(totalprice="abc")).status_code == 400


@known_issue("F-07", "negative price is accepted")
def test_should_reject_negative_price(bookings):
    assert bookings.create(new_booking(totalprice=-50)).status_code == 400


@known_issue("F-08", "check-out before check-in is accepted")
def test_should_reject_checkout_before_checkin(bookings):
    dates = {"checkin": "2027-02-10", "checkout": "2027-02-01"}
    assert bookings.create(new_booking(bookingdates=dates)).status_code == 400


@known_issue("F-09", "invalid date is stored as 0NaN-aN-aN")
def test_should_reject_invalid_date(bookings):
    dates = {"checkin": "not-a-date", "checkout": "2027-02-01"}
    assert bookings.create(new_booking(bookingdates=dates)).status_code == 400
