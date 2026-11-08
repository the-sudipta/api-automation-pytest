import pytest

pytestmark = pytest.mark.booker


def ids_of(response) -> list[int]:
    return [item["bookingid"] for item in response.json()]


def test_should_find_booking_by_first_and_last_name(bookings, created_booking):
    booking = created_booking["booking"]
    response = bookings.list_ids(firstname=booking["firstname"], lastname=booking["lastname"])
    assert response.status_code == 200
    assert ids_of(response) == [created_booking["bookingid"]]


def test_should_include_booking_when_filtering_by_its_dates(bookings, created_booking):
    dates = created_booking["booking"]["bookingdates"]
    response = bookings.list_ids(checkin=dates["checkin"])
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_should_return_empty_list_for_unknown_name(bookings):
    response = bookings.list_ids(firstname="Nobody", lastname="Matches-This-Name-xyz")
    assert response.status_code == 200
    assert response.json() == []
