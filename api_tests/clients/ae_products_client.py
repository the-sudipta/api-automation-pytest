"""Products, brands and search endpoints of the Automation Exercise API (APIs 1-6)."""

import requests

from api_tests.http_session import ApiSession


class AeProductsClient:
    def __init__(self, session: ApiSession) -> None:
        self.session = session

    def products(self) -> requests.Response:
        return self.session.get("/productsList")

    def brands(self) -> requests.Response:
        return self.session.get("/brandsList")

    def search(self, term: str | None) -> requests.Response:
        data = {"search_product": term} if term is not None else None
        return self.session.post("/searchProduct", data=data)

    def call(self, method: str, path: str) -> requests.Response:
        """Any method on any path; used for the "method not supported" checks."""
        return self.session.request(method, path)
