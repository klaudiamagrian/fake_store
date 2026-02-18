import pytest
import pymysql
from fake_store.app.product_repo import ProductRepo

# test 1 - save i get product
def test_save_and_get_product():
    repo = ProductRepo()

    repo.ensure_schema()
    repo.clear()

    product = {
        "id": 1,
        "name": "Laptop",
        "price_net": 100.0,
        "price_gross": 123.0
    }

    repo.save(product)
    result = repo.get(1)

    assert result == product

# test 2 - get, gdy product nie istnieje
def test_get_when_product_not_exist():
    repo = ProductRepo()
    repo.ensure_schema()
    repo.clear()

    result = repo.get(999)
    assert result is None

# test 3 - update istniejącego produktu
def test_update_existing_product():
    repo = ProductRepo()
    repo.ensure_schema()
    repo.clear()

    product = {
        "id": 1,
        "name": "Laptop",
        "price_net": 100,
        "price_gross": 123
    }

    repo.save(product)

    update_product = {
        "id": 1,
        "name": "Laptop Lenovo",
        "price_net": 200,
        "price_gross": 223
    }

    result = repo.update(update_product)

    saved_product = repo.get(1)

    assert result is True
    assert saved_product["name"] == "Laptop Lenovo"

#test 4 - update nieistniejącego produktu
def test_update_not_existing_product():
    repo = ProductRepo()
    repo.ensure_schema()
    repo.clear()

    updated_product = {
        "id": 1,
        "name": "Macbook",
        "price_net": 200,
        "price_gross": 223
    }

    result = repo.update(updated_product)

    assert result is False

# test 5 - usuwanie istniejącego rpoduktu
def test_delete_existing_product():
    repo = ProductRepo()
    repo.ensure_schema()
    repo.clear()

    product = {
        "id": 1,
        "name": "Laptop",
        "price_net": 200,
        "price_gross": 223
    }

    stworzony_produkt = repo.save(product)
    usuniecie_produktu = repo.delete(1)

    assert usuniecie_produktu is True
    assert repo.get(1) is None

# test 6 - usuniecie nieistniejacego produktu
def test_delete_not_existing_product():
    repo = ProductRepo()
    repo.ensure_schema()
    repo.clear()

    result = repo.delete(99)

    assert result is False

