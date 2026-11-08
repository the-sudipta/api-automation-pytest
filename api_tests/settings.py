"""Settings from environment variables (and an optional .env file); defaults point at the public APIs."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    booker_base_url: str
    booker_username: str
    booker_password: str
    ae_base_url: str
    timeout: float
    in_ci: bool


def load_settings() -> Settings:
    return Settings(
        booker_base_url=os.getenv("BOOKER_BASE_URL", "https://restful-booker.herokuapp.com").rstrip("/"),
        # Demo credentials published in the Restful Booker API documentation.
        booker_username=os.getenv("BOOKER_USERNAME", "admin"),
        booker_password=os.getenv("BOOKER_PASSWORD", "password123"),
        ae_base_url=os.getenv("AE_BASE_URL", "https://automationexercise.com/api").rstrip("/"),
        timeout=float(os.getenv("REQUEST_TIMEOUT", "30")),
        in_ci=os.getenv("CI", "").lower() == "true",
    )
