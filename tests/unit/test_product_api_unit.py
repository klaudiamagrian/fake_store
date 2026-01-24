import pytest
from app.product_service_api import ProductService

def test_compute_gross_price_positive():
    service = ProductService(None, None)
    assert service.compute_gross_price(100) == 123

def test_compute_gross_price_negative():
    service = ProductService(None, None)
    with pytest.raises(ValueError):
        service.compute_gross_price(-100)

def test_compute_gross_price_rounding():
    service = ProductService(None, None)
    assert service.compute_gross_price(9.99) == 12.29

def test_compute_gross_price_invalid():
    service = ProductService(None, None)
    with pytest.raises(ValueError):
        service.compute_gross_price(0)

