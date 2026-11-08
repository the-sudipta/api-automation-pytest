"""CRUD chain: create -> read -> update (PUT) -> partial update (PATCH) -> delete -> 404."""

import pytest

from api_tests.data.bookings import new_booking

pytestmark = pytest.mark.booker

BASIC_AUTH = {
    "Accept": "application/json",
    "Authorization": "Basic YWRtaW46cGFzc3dvcmQxMjM=",
}  # admin:password123


@pytest.mark.smoke
def test_should_create_booking_and_echo_the_data(bookings, authorized_bookings):
    body = new_booking()
    response = bookings.create(body)
    assert response.status_code == 200  # documented as 200 in /apidoc
    created = response.json()
    assert created["booking"] == body
    authorized_bookings.delete(created["bookingid"])


@pytest.mark.smoke
def test_should_read_back_the_created_booking(bookings, created_booking):
    response = bookings.get(created_booking["bookingid"])
    assert response.status_code == 200
    assert response.json() == created_booking["booking"]


def test_should_replace_booking_with_put(authorized_bookings, bookings, created_booking):
    replacement = new_booking(firstname="Farhana", totalprice=480, additionalneeds="Airport pickup")
    response = authorized_bookings.update(created_booking["bookingid"], replacement)
    assert response.status_code == 200
    assert response.json() == replacement
    assert bookings.get(created_booking["bookingid"]).json() == replacement


def test_should_change_only_sent_fields_with_patch(authorized_bookings, created_booking):
    response = authorized_bookings.partial_update(created_booking["bookingid"], {"totalprice": 333})
    assert response.status_code == 200
    assert response.json() == {**created_booking["booking"], "totalprice": 333}


def test_should_accept_basic_auth_for_patch(bookings, created_booking):
    response = bookings.partial_update(
        created_booking["bookingid"], {"additionalneeds": "Extra pillow"}, BASIC_AUTH
    )
    assert response.status_code == 200
    assert response.json()["additionalneeds"] == "Extra pillow"


@pytest.mark.smoke
def test_should_delete_booking_and_then_return_404(bookings, authorized_bookings):
    booking_id = bookings.create(new_booking()).json()["bookingid"]
    assert authorized_bookings.delete(booking_id).status_code == 201  # documented as 201 in /apidoc
    assert bookings.get(booking_id).status_code == 404
