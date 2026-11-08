import pytest

from api_tests.models.booking import Token
from tests.conftest import known_issue

pytestmark = pytest.mark.booker


@pytest.mark.smoke
def test_should_return_token_for_valid_credentials(auth, settings):
    response = auth.create_token(settings.booker_username, settings.booker_password)
    assert response.status_code == 200
    Token.model_validate(response.json())


@pytest.mark.negative
@pytest.mark.parametrize(
    ("username", "password"),
    [("admin", "wrong-password"), ("unknown-user", "password123"), ("", ""), ("ADMIN", "password123")],
    ids=["wrong password", "unknown user", "empty fields", "username in upper case"],
)
def test_should_not_return_token_for_invalid_credentials(auth, username, password):
    body = auth.create_token(username, password).json()
    assert "token" not in body
    assert body == {"reason": "Bad credentials"}


@pytest.mark.negative
@known_issue("F-01", "wrong credentials return 200 instead of 401")
def test_should_answer_401_for_wrong_password(auth):
    assert auth.create_token("admin", "wrong-password").status_code == 401
