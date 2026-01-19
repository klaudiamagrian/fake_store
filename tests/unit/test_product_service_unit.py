import pytest
from app.product_service import ProductService

def test_compute_gross_price_ok():
    service = ProductService(None, None)
    assert service.compute_gross_price(100) == 123.0

def test_compute_gross_price_rounding():
    service = ProductService(None, None)
    assert service.compute_gross_price(10.99) == 13.52

def test_compute_gross_price_invalid():
    service = ProductService(None, None)
    with pytest.raises(ValueError):
        service.compute_gross_price(0)
