"""Automation Exercise API contract as typed models."""

from pydantic import BaseModel, ConfigDict, Field


class UserType(BaseModel):
    usertype: str


class Category(BaseModel):
    usertype: UserType
    category: str


class Product(BaseModel):
    id: int
    name: str = Field(min_length=1)
    price: str = Field(pattern=r"^Rs\. \d+$")
    brand: str = Field(min_length=1)
    category: Category


class ProductList(BaseModel):
    responseCode: int  # noqa: N815 - field name defined by the API
    products: list[Product]


class Brand(BaseModel):
    id: int
    brand: str = Field(min_length=1)


class BrandList(BaseModel):
    responseCode: int  # noqa: N815
    brands: list[Brand]


class Message(BaseModel):
    model_config = ConfigDict(extra="forbid")
    responseCode: int  # noqa: N815
    message: str = Field(min_length=1)


class User(BaseModel):
    id: int
    name: str
    email: str
    first_name: str
    last_name: str
    city: str
    country: str


class UserDetail(BaseModel):
    responseCode: int  # noqa: N815
    user: User
