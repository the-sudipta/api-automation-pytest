"""Account endpoints of the Automation Exercise API (APIs 7-14)."""

import requests

from api_tests.data.users import AeUser
from api_tests.http_session import ApiSession


class AeAccountClient:
    def __init__(self, session: ApiSession) -> None:
        self.session = session

    def create(self, user: AeUser) -> requests.Response:
        return self.session.post("/createAccount", data=user.form())

    def update(self, user: AeUser) -> requests.Response:
        return self.session.put("/updateAccount", data=user.form())

    def verify_login(self, email: str | None, password: str | None) -> requests.Response:
        data = {k: v for k, v in {"email": email, "password": password}.items() if v is not None}
        return self.session.post("/verifyLogin", data=data)

    def detail(self, email: str) -> requests.Response:
        return self.session.get("/getUserDetailByEmail", params={"email": email})

    def delete(self, email: str, password: str) -> requests.Response:
        return self.session.delete("/deleteAccount", data={"email": email, "password": password})
