"""Restful Booker contract as typed models."""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class BookingDates(StrictModel):
    checkin: date
    checkout: date


class Booking(StrictModel):
    firstname: str = Field(min_length=1)
    lastname: str = Field(min_length=1)
    totalprice: StrictInt
    depositpaid: StrictBool
    bookingdates: BookingDates
    additionalneeds: str | None = None

    def to_json(self) -> dict:
        return self.model_dump(mode="json", exclude_none=True)


class CreatedBooking(StrictModel):
    bookingid: StrictInt
    booking: Booking


class BookingId(StrictModel):
    bookingid: StrictInt


class Token(StrictModel):
    token: str = Field(pattern=r"^[a-f0-9]{15}$")
