from collections.abc import Iterator

import pytest

from api_tests.clients.ae_account_client import AeAccountClient
from api_tests.clients.ae_products_client import AeProductsClient
from api_tests.clients.auth_client import AuthClient
from api_tests.clients.booking_client import BookingClient
from api_tests.data.bookings import new_booking
from api_tests.data.users import AeUser
from api_tests.http_session import ApiSession
from api_tests.settings import Settings, load_settings

FINDINGS = "https://github.com/the-sudipta/api-testing-postman-newman/blob/main/docs/findings.md"


def known_issue(finding: str, text: str):
    """Expected failure for an API defect documented in my Postman project; strict, so a fix shows up."""
    return pytest.mark.xfail(reason=f"{finding}: {text} ({FINDINGS})", strict=True)


def pytest_html_report_title(report):
    report.title = "API Test Report - Restful Booker and Automation Exercise"


@pytest.fixture(scope="session")
def settings() -> Settings:
    return load_settings()


@pytest.fixture(scope="session")
def booker_session(settings) -> Iterator[ApiSession]:
    with ApiSession(settings.booker_base_url, settings.timeout, retry_in_ci=settings.in_ci) as session:
        yield session


@pytest.fixture(scope="session")
def ae_session(settings) -> Iterator[ApiSession]:
    with ApiSession(settings.ae_base_url, settings.timeout, retry_in_ci=settings.in_ci) as session:
        yield session


@pytest.fixture(scope="session")
def auth(booker_session) -> AuthClient:
    return AuthClient(booker_session)


@pytest.fixture(scope="session")
def token(auth, settings) -> str:
    return auth.token(settings.booker_username, settings.booker_password)


@pytest.fixture(scope="session")
def bookings(booker_session) -> BookingClient:
    """Client without a token: reads and negative checks."""
    return BookingClient(booker_session)


@pytest.fixture(scope="session")
def authorized_bookings(booker_session, token) -> BookingClient:
    return BookingClient(booker_session, token)


@pytest.fixture
def created_booking(bookings, authorized_bookings) -> Iterator[dict]:
    """A booking created for one test and deleted afterwards: {"bookingid": ..., "booking": {...}}."""
    response = bookings.create(new_booking())
    assert response.status_code == 200, response.text
    created = response.json()
    yield created
    authorized_bookings.delete(created["bookingid"])


@pytest.fixture(scope="session")
def ae_products(ae_session) -> AeProductsClient:
    return AeProductsClient(ae_session)


@pytest.fixture(scope="session")
def ae_accounts(ae_session) -> AeAccountClient:
    return AeAccountClient(ae_session)


@pytest.fixture
def ae_user(ae_accounts) -> Iterator[AeUser]:
    """A registered Automation Exercise user, deleted after the test."""
    user = AeUser()
    assert ae_accounts.create(user).json()["responseCode"] == 201
    yield user
    ae_accounts.delete(user.email, user.password)
