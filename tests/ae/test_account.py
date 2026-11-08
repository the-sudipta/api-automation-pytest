"""Automation Exercise APIs 7-14: account lifecycle and login checks."""

import pytest

from api_tests.data.users import AeUser
from api_tests.models.automation_exercise import Message, UserDetail

pytestmark = pytest.mark.ae


def message(response) -> Message:
    return Message.model_validate_json(response.text)


@pytest.mark.smoke
def test_registered_user_can_log_in(ae_accounts, ae_user):
    body = message(ae_accounts.verify_login(ae_user.email, ae_user.password))
    assert (body.responseCode, body.message) == (200, "User exists!")


@pytest.mark.negative
def test_second_account_with_same_email_is_refused(ae_accounts, ae_user):
    body = message(ae_accounts.create(ae_user))
    assert (body.responseCode, body.message) == (400, "Email already exists!")


def test_update_is_visible_in_user_details(ae_accounts, ae_user):
    assert message(ae_accounts.update(ae_user.moved_to("Chattogram"))).responseCode == 200
    detail = UserDetail.model_validate_json(ae_accounts.detail(ae_user.email).text)
    assert (detail.user.email, detail.user.city) == (ae_user.email, "Chattogram")
    assert (detail.user.first_name, detail.user.last_name) == (ae_user.firstname, ae_user.lastname)


def test_deleted_account_can_no_longer_log_in(ae_accounts):
    user = AeUser()
    ae_accounts.create(user)
    assert message(ae_accounts.delete(user.email, user.password)).message == "Account deleted!"
    assert message(ae_accounts.verify_login(user.email, user.password)).responseCode == 404
    assert message(ae_accounts.delete(user.email, user.password)).responseCode == 404


@pytest.mark.negative
@pytest.mark.parametrize(
    ("email", "password", "code", "text"),
    [
        ("nobody.qa.portfolio@example.com", "Wrong@123", 404, "User not found!"),
        (None, "Wrong@123", 400, "Bad request, email or password parameter is missing in POST request."),
        (
            "nobody.qa.portfolio@example.com",
            None,
            400,
            "Bad request, email or password parameter is missing in POST request.",
        ),
    ],
    ids=["unknown user", "missing email", "missing password"],
)
def test_invalid_logins_are_refused(ae_accounts, email, password, code, text):
    body = message(ae_accounts.verify_login(email, password))
    assert (body.responseCode, body.message) == (code, text)


@pytest.mark.negative
def test_wrong_password_for_registered_user_is_refused(ae_accounts, ae_user):
    body = message(ae_accounts.verify_login(ae_user.email, ae_user.password.upper()))
    assert body.responseCode == 404


@pytest.mark.negative
def test_details_of_unknown_email_are_not_found(ae_accounts):
    body = message(ae_accounts.detail("nobody.qa.portfolio@example.com"))
    assert (body.responseCode, body.message) == (404, "Account not found with this email, try another email!")
