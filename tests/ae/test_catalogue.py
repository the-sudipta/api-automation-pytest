"""Automation Exercise APIs 1-6: products, brands and search."""

import pytest

from api_tests.models.automation_exercise import BrandList, Message, ProductList
from tests.conftest import known_issue

pytestmark = pytest.mark.ae


@pytest.mark.smoke
@pytest.mark.contract
def test_product_list_follows_the_contract(ae_products):
    response = ae_products.products()
    assert response.status_code == 200
    products = ProductList.model_validate_json(response.text)
    assert products.responseCode == 200
    assert len(products.products) >= 30
    assert len({p.id for p in products.products}) == len(products.products), "product IDs must be unique"


@pytest.mark.contract
def test_brand_list_follows_the_contract(ae_products):
    brands = BrandList.model_validate_json(ae_products.brands().text)
    assert brands.responseCode == 200
    assert brands.brands


@pytest.mark.parametrize("term", ["top", "dress", "jean", "tshirt"])
def test_search_returns_only_related_products(ae_products, term):
    result = ProductList.model_validate_json(ae_products.search(term).text)
    assert result.products, f"no results for {term!r}"
    for product in result.products:
        text = f"{product.name} {product.category.category}".lower().replace("-", "")
        assert term in text, f"{product.name} ({product.category.category}) does not match {term!r}"


def test_search_without_match_returns_empty_list(ae_products):
    result = ProductList.model_validate_json(ae_products.search("zzzqqq").text)
    assert (result.responseCode, result.products) == (200, [])


@pytest.mark.negative
def test_search_without_parameter_is_a_bad_request(ae_products):
    body = Message.model_validate_json(ae_products.search(None).text)
    assert body.responseCode == 400
    assert "search_product parameter is missing" in body.message


@pytest.mark.negative
@pytest.mark.parametrize(
    ("method", "path"),
    [("POST", "/productsList"), ("PUT", "/brandsList"), ("DELETE", "/verifyLogin")],
    ids=["API 2", "API 4", "API 9"],
)
def test_unsupported_methods_are_refused(ae_products, method, path):
    body = Message.model_validate_json(ae_products.call(method, path).text)
    assert (body.responseCode, body.message) == (405, "This request method is not supported.")


@pytest.mark.negative
@known_issue("F-13", "HTTP status is always 200; the real code is only in the body")
def test_http_status_matches_the_error(ae_products):
    assert ae_products.call("POST", "/productsList").status_code == 405


@pytest.mark.contract
@known_issue("F-14", "JSON responses are served as text/html")
def test_responses_are_served_as_json(ae_products):
    assert ae_products.products().headers["Content-Type"].startswith("application/json")
