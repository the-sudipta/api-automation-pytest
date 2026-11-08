"""POST /auth of Restful Booker."""

import requests

from api_tests.http_session import ApiSession


class AuthClient:
    def __init__(self, session: ApiSession) -> None:
        self.session = session

    def create_token(self, username: str, password: str) -> requests.Response:
        return self.session.post("/auth", json={"username": username, "password": password})

    def token(self, username: str, password: str) -> str:
        body = self.create_token(username, password).json()
        if "token" not in body:
            raise AssertionError(f"No token returned: {body}")
        return body["token"]
