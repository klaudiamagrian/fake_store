import requests

BASE = "https://fakestoreapi.com/products"

def test_get_single_product():
    res = requests.get(f"{BASE}/1")
    assert res.status_code == 200

    product = res.json()
    assert product["id"] == 1
    assert "title" in product
    assert "price" in product

def test_get_all_products():
    res = requests.get(BASE)
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert len(res.json()) > 0
