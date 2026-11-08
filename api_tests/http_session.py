"""A requests Session with a base URL, a default timeout and request logging.

Retries are switched on only in CI (environment variable CI=true) and only for idempotent methods and gateway
errors, so a network blip on a shared runner does not fail the build, while local runs show every failure.
"""

import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

LOG = logging.getLogger("api")

CI_RETRY = Retry(
    total=2,
    backoff_factor=1,
    status_forcelist=(502, 503, 504),
    allowed_methods=frozenset({"GET", "PUT", "DELETE", "HEAD", "OPTIONS"}),
    raise_on_status=False,
)


class ApiSession(requests.Session):
    def __init__(self, base_url: str, timeout: float, retry_in_ci: bool) -> None:
        super().__init__()
        self.base_url = base_url
        self.timeout = timeout
        if retry_in_ci:
            adapter = HTTPAdapter(max_retries=CI_RETRY)
            self.mount("https://", adapter)
            self.mount("http://", adapter)

    def request(self, method, url, *args, **kwargs):  # type: ignore[override]
        kwargs.setdefault("timeout", self.timeout)
        full_url = url if url.startswith("http") else f"{self.base_url}{url}"
        response = super().request(method, full_url, *args, **kwargs)
        LOG.info("%s %s -> %s (%.0f ms)", method, full_url, response.status_code, elapsed_ms(response))
        return response


def elapsed_ms(response: requests.Response) -> float:
    return response.elapsed.total_seconds() * 1000
