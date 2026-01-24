from app.product_client import ProductClient

def test_get_product_by_id():
    product = ProductClient().get(1)
    assert product["id"] == 1
    assert product is not None
    assert product["title"] == "Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops"

def test_list_all_products():
    products = ProductClient().list_all()
    assert products is not None
    assert len(products) > 0
    assert products[0]["id"] == 1

