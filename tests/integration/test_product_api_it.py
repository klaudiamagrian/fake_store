from app.product_client import ProductClient
import pytest
import requests

def test_get_product_by_id_happy_path():
    product = ProductClient().get(1)
    assert product["id"] == 1
    assert product is not None
    assert product["title"] == "Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops"

def test_list_all_products_happy_path():
    products = ProductClient().list_all()
    assert products is not None
    assert len(products) > 0
    assert products[0]["id"] == 1

@pytest.mark.parametrize("invalid_id", ["abc", -1, 0])
def test_get_invalid_id_raises_valueerror(invalid_id):
    client = ProductClient()
    with pytest.raises(ValueError):
        client.get(invalid_id)

