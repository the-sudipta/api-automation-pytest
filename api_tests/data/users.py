"""Fake Automation Exercise user with a unique @example.com address."""

import uuid
from dataclasses import dataclass, field, replace


@dataclass(frozen=True)
class AeUser:
    name: str = "Tanvir"
    email: str = field(default_factory=lambda: f"qa.pytest.{uuid.uuid4().hex[:10]}@example.com")
    password: str = field(default_factory=lambda: f"Test@{uuid.uuid4().hex[:6]}")
    firstname: str = "Tanvir"
    lastname: str = "Ahmed"
    city: str = "Dhaka"
    country: str = "India"

    def form(self) -> dict:
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "title": "Mr",
            "birth_date": "10",
            "birth_month": "May",
            "birth_year": "1998",
            "firstname": self.firstname,
            "lastname": self.lastname,
            "company": "QA Practice",
            "address1": "House 12, Road 5",
            "address2": "Dhanmondi",
            "country": self.country,
            "zipcode": "1207",
            "state": "Dhaka",
            "city": self.city,
            "mobile_number": "01712345678",
        }

    def moved_to(self, city: str) -> "AeUser":
        return replace(self, city=city)
