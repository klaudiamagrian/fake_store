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

def test_get_product_id_not_found():
    client = ProductClient()
    non_existent_id = 9999
    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        client.get(non_existent_id)


# @pytest.mark.parametrize("method_name, arg", [("get", 1), ("list_all", None)])
# @patch("app.product_client.requests.get")
# def test_http_error(mock_get, method_name, arg):
#     mock_response = Mock()
#     mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("HTTP Error")
#     mock_get.return_value = mock_response

#     client = ProductClient()
#     if method_name == "get":
#         with pytest.raises(requests.exceptions.HTTPError):
#             client.get(arg)
#     else:
#         with pytest.raises(requests.exceptions.HTTPError):
#             client.list_all()

# @patch("app.product_client.requests.get")
# def test_list_all_empty(mock_get):
#     mock_response = Mock()
#     mock_response.raise_for_status.return_value = None
#     mock_response.json.return_value = []
#     mock_get.return_value = mock_response

#     client = ProductClient()
#     products = client.list_all()
#     assert products == []