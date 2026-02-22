import pytest
from app.product_service import ProductService

class FakeBaza:
    def __init__(self):
        self.saved_product = None
        self.snapshot_called = False
        self.external_lookup = None
        self.best_deals_result = []
        self.best_deals_called_with = None

        # NOWE POLA DO UPDATE
        self.product = None
        self.updated_product = None

    def get_by_external_id(self, external_id):
        return self.external_lookup

    def save(self, product):
        product["id"] = 1
        self.saved_product = product

    def get(self, product_id):
        return self.product

    def update(self, product):
        self.updated_product = product
        return True

    def add_price_snapshot(self, product_id, price_net, price_gross):
        self.snapshot_called = True

    def delete(self, product_id):
        self.delete_called = True
        return self.delete_result

    def get_best_deals(self, limit):
        self.best_deals_called_with = limit
        return self.best_deals_result

# w main - 1. dodanie produktu ręcznie:
# a) happy path
def test_create_product_sukces():
    baza = FakeBaza()
    service = ProductService(baza)

    nowy_produkt = service.create_product("Laptop", 1000)

    assert nowy_produkt["id"] == 1
    assert nowy_produkt["name"] == "Laptop"
    assert nowy_produkt["price_net"] == 1000.0
    assert nowy_produkt["price_gross"] == 1230.0  # VAT 23%
    assert baza.snapshot_called is True

# b) za krótka nazwa (ValueError, gdy mniej niż 3 znaki)
def test_create_product_za_krotka_nazwa():
    baza = FakeBaza()
    service = ProductService(baza)

    with pytest.raises(ValueError):
        service.create_product("Ka", 1000)

# c) niepoprawna cena, gdy:
# - równa 0,
# - mniejsza od 0,
# - większa niż maksymalna cena (50_000)
@pytest.mark.parametrize("price", [0, -10, 100000])
def test_create_product_niepoprawna_cena(price):
    baza = FakeBaza()
    service = ProductService(baza)

    with pytest.raises(ValueError):
        service.create_product("Laptop", price)

# w main - 4. aktualizuj cenę produktu:
# a) happy path
def test_update_price_sukces():
    baza = FakeBaza()
    baza.product = {
        "id": 1,
        "name": "Laptop",
        "price_net": 1000.0,
        "price_gross": 1230.0
    }

    service = ProductService(baza)

    zaktualizowany = service.update_price(1, 2000)

    assert zaktualizowany["price_net"] == 2000.0
    assert zaktualizowany["price_gross"] == 2460.0  # 2000 * 1.23
    assert baza.updated_product["price_net"] == 2000.0
    assert baza.snapshot_called is True

# b) obsługa błędu => produkt o tym id nie istnieje
def test_update_price_product_nie_istnieje():
    baza = FakeBaza()
    baza.product = None

    service = ProductService(baza)

    with pytest.raises(ValueError, match="Product not found"):
        service.update_price(1, 2000)

# w main -> 5. zmień nazwę produktu
# a) happy path
def test_rename_product_sukces():
    baza = FakeBaza()
    baza.product = {
        "id": 1,
        "name": "Książka",
        "price_net": 100,
        "price_gross": 123
    }

    service = ProductService(baza)

    zaktualizowany = service.rename_product(1, "Książka harry potter")

    assert zaktualizowany["name"] == "Książka harry potter"
    assert baza.updated_product["name"] == "Książka harry potter"

# b) obsługa błędu -> ValueError jeśli produkt nie istnieje
def test_rename_product_product_nie_istnieje():
    baza = FakeBaza()
    baza.product = None

    service = ProductService(baza)

    with pytest.raises(ValueError, match="Product not found"):
        service.rename_product(1, "New Name")

# w main: 6. Zastosuj rabat
# a) hapy path
def test_apply_discount_sukces():
    baza = FakeBaza()
    baza.product = {
        "id": 1,
        "name": "Laptop",
        "price_net": 1000.0,
        "price_gross": 1230.0
    }

    service = ProductService(baza)

    zaktualizowany = service.apply_discount(1, 10)  # 10% rabatu

    assert zaktualizowany["price_net"] == 900.0
    assert zaktualizowany["price_gross"] == 1107.0  # 900 * 1.23
    assert baza.updated_product["price_net"] == 900.0
    assert baza.snapshot_called is True

# obsługa błędu -> jeśli rabat <= 0 i >= 90 = ValueError
@pytest.mark.parametrize("percent", [0, -5, 90, 100])
def test_apply_discount_niepoprawny_procent(percent):
    baza = FakeBaza()
    service = ProductService(baza)

    with pytest.raises(ValueError, match="Invalid discount value"):
        service.apply_discount(1, percent)

# z main: 7. Usuń produkt
# a) happy path
def test_delete_product_sukces():
    baza = FakeBaza()
    baza.product = {"id": 1}
    baza.delete_result = True

    service = ProductService(baza)

    result = service.delete_product(1)

    assert result is True
    assert baza.delete_called is True

# w main: 10. Ranking best deals (największy spadek ceny)
# a) happy path
def test_best_deals_sukces():
    baza = FakeBaza()
    baza.best_deals_result = [
        {"id": 1, "drop_net": 200},
        {"id": 2, "drop_net": 150},
    ]

    service = ProductService(baza)

    result = service.best_deals(5)

    assert result == baza.best_deals_result
    assert baza.best_deals_called_with == 5

# b) obsługa błędu - dodać opis
@pytest.mark.parametrize("limit", [0, -5, 51, 100])
def test_best_deals_invalid_limit_lower(limit):
    baza = FakeBaza()
    service = ProductService(baza)

    with pytest.raises(ValueError, match="Invalid limit"):
        service.best_deals(limit)