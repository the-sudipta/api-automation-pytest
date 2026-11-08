"""/booking resource of Restful Booker."""

import requests

from api_tests.http_session import ApiSession

JSON = {"Accept": "application/json"}


class BookingClient:
    def __init__(self, session: ApiSession, token: str | None = None) -> None:
        self.session = session
        self.token = token

    def _auth_headers(self) -> dict:
        return {**JSON, "Cookie": f"token={self.token}"} if self.token else dict(JSON)

    def list_ids(self, **filters: str) -> requests.Response:
        return self.session.get("/booking", params=filters, headers=JSON)

    def get(self, booking_id: int | str) -> requests.Response:
        return self.session.get(f"/booking/{booking_id}", headers=JSON)

    def create(self, body: dict | str) -> requests.Response:
        if isinstance(body, str):
            headers = {**JSON, "Content-Type": "application/json"}
            return self.session.post("/booking", data=body, headers=headers)
        return self.session.post("/booking", json=body, headers=JSON)

    def update(self, booking_id: int, body: dict) -> requests.Response:
        return self.session.put(f"/booking/{booking_id}", json=body, headers=self._auth_headers())

    def partial_update(self, booking_id: int, fields: dict, headers: dict | None = None) -> requests.Response:
        return self.session.patch(
            f"/booking/{booking_id}", json=fields, headers=headers or self._auth_headers()
        )

    def delete(self, booking_id: int, headers: dict | None = None) -> requests.Response:
        return self.session.delete(f"/booking/{booking_id}", headers=headers or self._auth_headers())
