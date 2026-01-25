import pytest
from app.product_service import ProductService

# TESTY: METODA NR 1 - NORMALIZE_NAME

# METODA NR 1 - test 1 => happy path "Laptop" = "Laptop"
def test_normalize_name_happy_path():
    service = ProductService(None)
    assert service.normalize_name("Laptop") == "Laptop"

# METODA NR 1 - test 2 => usuwanie nadmiarowych spacji z początku, środka i końca string
def test_normalize_name_delete_too_many_spaces():
    service = ProductService(None)
    assert service.normalize_name("    Laptop    Apple    MacBook     ") == "Laptop Apple MacBook"

# METODA NR 1 - test 3 => zwrot pustego stringa, jeśli jest początkowo pusty
def test_normalize_name_empty_string():
    service = ProductService(None)
    assert service.normalize_name("") == ""

# METODA NR 1 - test 4 => jeśli None => wynik = "" (pusty string)
def test_normalize_name_if_none_then_empty_string():
    service = ProductService(None)
    assert service.normalize_name(None) == ""

# METODA NR 1 - test 4 => test parametryczny - w zasadzie sprawdza to samo, co powyższe
@pytest.mark.parametrize("input_name, expected",
    [
        ("Laptop", "Laptop"),
        ("  Laptop  ", "Laptop"),
        ("  Laptop   Pro ", "Laptop Pro"),
        ("", ""),
        (None, ""),
    ],
)
def test_normalize_name_parametrized(input_name, expected):
    service = ProductService(None)
    assert service.normalize_name(input_name) == expected

# TESTY: METODA NR 2 - VALIDATE_NAME

# METODA NR 2 - test 1 => (przypadek brzegowy) najmniejszy dopuszczalny string (ilość znaków = 3) i sprawdzenie usuwania spacji z końca i początku stringa
def test_validate_name_min_length():
    service = ProductService(None)
    assert service.validate_name("   Tel     ") == "Tel"

# METODA NR 2 - test 2 => ValueError -> gdy długość string < 3
def test_validate_name_length_less_than_three():
    service = ProductService(None)
    with pytest.raises(ValueError):
        assert service.validate_name("La")

# METODA NR 2 - test 3 => ValueError, jeśli ilość większa niż MAX_NAME_LENGTH = 80
def test_validate_name_above_max_length():
    service = ProductService(None)
    with pytest.raises(ValueError):
        assert service.validate_name("A" * 81)

# METODA NR 2 - test 4 => (przypadek brzegowy) nie daje ValueError, jeśli długość string = 80
def test_validate_name_string_has_max_length():
    service = ProductService(None)
    assert service.validate_name("A" * 80) == "A" * 80

# METODA NR 2 - test 5 => ValueError, gdy string jest pusty
def test_validate_name_string_is_empty():
    service = ProductService(None)
    with pytest.raises(ValueError):
        service.validate_name("")

# METODA NR 2 - test 6 => ValueError, gdy w stringu same spacje
def test_validate_name_string_has_only_spaces():
    service = ProductService(None)
    with pytest.raises(ValueError):
        service.validate_name("       ")

# METODA NR 2 - test 7 => ValueError, gdy string = None
def test_validate_name_string_is_none():
    service = ProductService(None)
    with pytest.raises(ValueError):
        service.validate_name(None)

# TESTY: METODA NR 3 - VALIDATE_PRICE_NET

# METODA NR 3 - test 1 => ValueError, jeśli price_net to string
def test_validate_price_net_is_string():
    service = ProductService(None)
    with pytest.raises(ValueError):
        service.validate_price_net("123")

# METODA NR 3 - test 2 => ValueError, jeśli price_net = None
def test_validate_price_net_is_none():
    service = ProductService(None)
    with pytest.raises(ValueError):
        service.validate_price_net(None)

# METODA NR 3 - test 3 => (przypadek brzegowy) ValueError, jeśli price_net = 0
def test_validate_price_net_is_zero():
    service = ProductService(None)
    with pytest.raises(ValueError):
        service.validate_price_net(0)

# METODA NR 3 - test 4 => ValueError, jeśli price_net < 0
def test_validate_price_net_is_below_zero():
    service = ProductService(None)
    with pytest.raises(ValueError):
        service.validate_price_net(-7)

# METODA NR 3 - test 5 => happy path - zaokrąglenie do 2 miejsc po przecinku
def test_validate_price_net_happy_path():
    service = ProductService(None)
    price_net = service.validate_price_net(19.999)
    assert price_net == 20.00

# METODA NR 3 - test 6 => happy path - int zamiast float
def test_validate_price_is_int():
    service = ProductService(None)
    price_net = service.validate_price_net(100)
    assert price_net == 100.00

# METODA NR 3 - test 7 => ValueError, jeśli price_net > MAX_PRICE = 50000
def test_validate_price_is_bigger_than_max_price():
    service = ProductService(None)
    with pytest.raises(ValueError):
        service.validate_price_net(50001)

# METODA NR 3 - test 8 => (przypadek brzegowy) jeśli price_net = MAX_PRICE = 50000
def test_validate_price_is_max_price():
    service = ProductService(None)
    price_net = service.validate_price_net(50000)
    assert price_net == 50000

# METODA NR 3 - test 9 => ValueError, jeśli price_net to lista (może być tylko int lub float)
def test_validate_price_is_list():
    service = ProductService(None)
    with pytest.raises(ValueError):
        service.validate_price_net([1])

# METODA NR 3 - test 10 => test parametryczny - poprawne wartości
@pytest.mark.parametrize(
    "price, expected",
    [
        (10, 10.00),
        (19.999, 20.00),
        (50000, 50000.00),
    ],
)
def test_validate_price_net_valid(price, expected):
    service = ProductService(None)
    assert service.validate_price_net(price) == expected

# TESTY: METODA NR 4 - VALIDATE_PRICE_GROSS

# METODA NR 4 - test 1 => happy path
def test_validate_price_gross():
    service = ProductService(None)
    assert service.validate_price_gross(100, 123.00) == 123.00

# METODA NR 4 - test 2 => (przypadek brzegowy) sprawdza niższą tolerancję błędu obliczenia
def test_validate_price_gross_lower_tolerance():
    service = ProductService(None)
    assert service.validate_price_gross(100, 122.95) == 122.95

# METODA NR 4 - test 3 => (przypadek brzegowy) sprawdza wyższą tolerancję błędu obliczenia
def test_validate_price_gross_upper_tolerance():
    service = ProductService(None)
    assert service.validate_price_gross(100, 123.05) == 123.05

# METODA NR 4 - test 4 => sprawdza, czy zaokrągla do w miejsc po przecinku
def test_validate_price_gross_rounding():
    service = ProductService(None)
    assert service.validate_price_gross(100, 123.049) == 123.05

# METODA NR 4 - test 5 => ValueError, jeśli poniżej tolerencji błędu
def test_validate_price_gross_below_mistake_tolerance():
    service = ProductService(None)
    with pytest.raises(ValueError):
        service.validate_price_gross(100, 122.94)

# METODA NR 4 - test 6 => ValueError, jeśli powyżej tolerencji błędu
def test_validate_price_gross_under_mistake_tolerance():
    service = ProductService(None)
    with pytest.raises(ValueError):
        service.validate_price_gross(100, 123.06)

# METODA NR 4 - test 7 => test paramateryczny - poprawne wartości
@pytest.mark.parametrize(
    "price_net, price_gross",
    [
        (100, 123.00),
        (100, 122.95),
        (100, 123.05),
        (100, 123.049),
    ],
)
def test_validate_price_gross_valid(price_net, price_gross):
    service = ProductService(None)
    result = service.validate_price_gross(price_net, price_gross)
    assert isinstance(result, float)


# TESTY: METODA NR 5 - COMPUTE_GROSS_PRICE

# METODA NR 5 - test 1 => happy path
def test_compute_gross_price_happy_path():
    service = ProductService(None)
    result = service.compute_gross_price(100)
    assert result == 123.00

# METODA NR 5 - test 2 => zaokrąglenie
def test_compute_gross_price_rounding():
    service = ProductService(None)
    result = service.compute_gross_price(19.99) # gross_price = 19.99 * 1.23 = 24.5877
    assert result == 24.59

# METODA NR 5 - test 3 => price_net = 0
def test_compute_gross_price_is_zero():
    service = ProductService(None)
    result = service.compute_gross_price(0)
    assert result == 0.00

# TESTY: METODA NR 6 - COMPUTE_MARGIN

# METODA NR 6 - test 1 => happy path - marża istnieje (sprzedaż drożej)
def test_compute_margin_happy_sell_more_expensive():
    service = ProductService(None)
    result = service.compute_margin(100, 150)
    assert result == 50.0

# METODA NR 6 - test 2 => brak marży (cena taka sama)
def test_compute_margin_happy_sell_same_price():
    service = ProductService(None)
    result = service.compute_margin(100, 100)
    assert result == 0.0

# METODA NR 6 - test 3 => minusowa marża (sprzedaż taniej)
def test_compute_margin_happy_sell_cheaper():
    service = ProductService(None)
    result = service.compute_margin(100, 80)
    assert result == -20.00

# METODA NR 6 - test 4 => wartości zmiennoprzecinkowe
def test_compute_margin_float():
    service = ProductService(None)
    result = service.compute_margin(19.99, 29.99)
    assert result == round(((29.99 - 19.99) / 19.99) * 100, 2)

# METODA NR 6 - test 5 => zaokrąglenie do 2 miejsc po przecinku
def test_compute_margin_rounding():
    service = ProductService(None)
    result = service.compute_margin(3, 4)
    # (4 - 3) / 3 * 100 = 33.333...
    assert result == 33.33

# METODA NR 6 - test 6 => (przypadek brzegowy) Value error - buy_price = 0
def teste_compute_margin_buy_price_is_zero():
    service = ProductService(None)
    with pytest.raises(ValueError):
        service.compute_margin(0, 10)

# METODA NR 6 - test 7 =>  Value error - buy_price < 0
def teste_compute_margin_buy_price_is_below_zero():
    service = ProductService(None)
    with pytest.raises(ValueError):
        service.compute_margin(-80, 10)

# METODA NR 6 - test 8 => sell_price = 0 (dozwolone) => wynik -100% buy_price
def test_compute_margin_sell_price_is_zero():
    service = ProductService(None)
    result = service.compute_margin(100, 0)
    assert result == -100.00

# METODA NR 6 - test 9 => sell_price < 0 (matematycznie poprawne)
def compyte_margin_sell_price_below_zero():
    service = ProductService(None)
    result = service.compute_margin(100, -50)
    assert result == -150.00

# METODA NR 6 - test 10 => test parametryczny - happy path
@pytest.mark.parametrize(
    "buy, sell, expected",
    [
        (100, 150, 50.00),
        (100, 100, 0.00),
        (100, 80, -20.00),
        (3, 4, 33.33),
    ],
)
def test_compute_margin_parametrized(buy, sell, expected):
    service = ProductService(None)
    assert service.compute_margin(buy, sell) == expected

# TESTY: METODA NR 7 - CREATE_PRODUCT

# Do poniższych metod (od 7 do 11) jest potrzebne repozytorium typu Fake:
class FakeProductRepo:
    def __init__(self):
        self.data = {}

    def get(self, product_id):
        return self.data.get(product_id)

    def save(self, product):
        self.data[product["id"]] = product

    def update(self, product):
        self.data[product["id"]] = product

    def delete(self, product_id):
        if product_id not in self.data:
            return False

        del self.data[product_id]
        return True

# METODA NR 7 - test 1 =>  happy path - stworzenie produktu
def test_create_product_happy_path():
    repo = FakeProductRepo()
    service = ProductService(repo)

    product = service.create_product(
        product_id = 1,
        name = "Laptop",
        price_net = 100
    )

    assert product["id"] == 1
    assert product["name"] == ("Laptop")
    assert product["price_net"] == 100.00
    assert product["price_gross"] == 123.00
    assert repo.get(1) is not None

# METODA NR 7 - test 2 => próba dodania istniejącego produktu
def test_create_product_already_exists():
    repo = FakeProductRepo()
    repo.save({"id": 1})

    service = ProductService(repo)

    with pytest.raises(ValueError):
        service.create_product(1, "Laptop", 100)

# METODA NR 7 - test 3 => niepoprawne imię (mniej niż 3 litery)
def test_create_product_invalid_name():
    repo = FakeProductRepo()
    service = ProductService(repo)

    with pytest.raises(ValueError):
        service.create_product(1, "AB", 100)

# METODA NR 7 - test 4 => price_net nie może być <= 0
def test_create_product_invalid_price():
    repo = FakeProductRepo()
    service = ProductService(repo)

    with pytest.raises(ValueError):
        service.create_product(1, "Laptop", -10)

# TESTY: METODA NR 8 - UPDATE_PRICE

# METODA NR 8 - test 1 => happy path - poprawny update produktu
def test_update_price_success():
    repo = FakeProductRepo()

    repo.save({
        "id": 1,
        "name": "Laptop",
        "price_net": 100.00,
        "price_gross": 123.00
    })

    service = ProductService(repo)

    updated = service.update_price(1, 200)

    assert updated["price_net"] == 200.00
    assert updated["price_gross"] == 246.00
    assert repo.get(1)["price_net"] == 200.00

# METODA NR 8 - test 2 => próba update'owania produktu nieistniejącego
def test_update_price_product_not_found():
    repo = FakeProductRepo()
    service = ProductService(repo)

    with pytest.raises(ValueError):
        service.update_price(1, 100)

# METODA NR 8 - test 3 => nowe cena nie może być ujemna
def test_update_price_invalid_price_negative():
    repo = FakeProductRepo()

    repo.save({
        "id": 1,
        "name": "Laptop",
        "price_net": 100,
        "price_gross": 123
    })

    service = ProductService(repo)

    with pytest.raises(ValueError):
        service.update_price(1, -10)


# METODA NR 8 - test 4 => nowa cena nie może być = 0
def test_update_price_invalid_price_zero():
    repo = FakeProductRepo()

    repo.save({
        "id": 1,
        "name": "Laptop",
        "price_net": 100,
        "price_gross": 123
    })

    service = ProductService(repo)

    with pytest.raises(ValueError):
        service.update_price(1, 0)


# METODA NR 8 - test 5 => zaokrąglenie ceny netto
def test_update_price_rounding():
    repo = FakeProductRepo()

    repo.save({
        "id": 1,
        "name": "Laptop",
        "price_net": 100,
        "price_gross": 123
    })

    service = ProductService(repo)

    updated = service.update_price(1, 19.999)

    assert updated["price_net"] == 20.00
    assert updated["price_gross"] == 24.60

# TESTY: METODA NR 9 - RENAME_PRODUCT

# METODA NR 9 - test 1 => happy path - poprawnie zmieniona nazwa produktu
def test_rename_product_success():
    repo = FakeProductRepo()
    repo.save({
        "id": 1,
        "name": "Old Name",
        "price_net": 100,
        "price_gross": 123
    })

    service = ProductService(repo)

    updated = service.rename_product(1, "New Product Name")

    assert updated["name"] == "New Product Name"
    assert repo.get(1)["name"] == "New Product Name"

# METODA NR 9 - test 2 => próba zmieny nazwy produktu nieistniejącego
def test_rename_product_not_found():
    repo = FakeProductRepo()
    service = ProductService(repo)

    with pytest.raises(ValueError):
        service.rename_product(1, "New Name")


# METODA NR 9 - test 3 => nowa nazwa za krótka (mniejsza niż 3 znaki)
def test_rename_product_name_too_short():
    repo = FakeProductRepo()
    repo.save({
        "id": 1,
        "name": "Old",
        "price_net": 100,
        "price_gross": 123
    })

    service = ProductService(repo)

    with pytest.raises(ValueError):
        service.rename_product(1, "AB")


# METODA NR 9 - test 4 => nazwa za długa (większa niż MAX_LENGTH = 80)
def test_rename_product_name_too_long():
    repo = FakeProductRepo()
    repo.save({
        "id": 1,
        "name": "Old",
        "price_net": 100,
        "price_gross": 123
    })

    service = ProductService(repo)

    with pytest.raises(ValueError):
        service.rename_product(1, "A" * 81)


# METODA NR 9 - test 5 => normalizacja nazwy (usuwanie spacji)
def test_rename_product_name_normalization():
    repo = FakeProductRepo()
    repo.save({
        "id": 1,
        "name": "Old",
        "price_net": 100,
        "price_gross": 123
    })

    service = ProductService(repo)

    updated = service.rename_product(1, "   New     Product   ")

    assert updated["name"] == "New Product"

# TESTY: METODA NR 10 - APPLY_DISCOUNT

# METODA NR 10 - test 1 => happy path - poprawne zastosowanie rabatu 10% do istniejącego produktu
def test_apply_discount_success():
    repo = FakeProductRepo()
    repo.save({
        "id": 1,
        "name": "Laptop",
        "price_net": 100.00,
        "price_gross": 123.00
    })

    service = ProductService(repo)

    updated = service.apply_discount(1, 10)

    assert updated["price_net"] == 90.00
    assert updated["price_gross"] == 110.70
    assert repo.get(1)["price_net"] == 90.00


# METODA NR 10 – test 2 => (przypadek brzegowy) minimalna dodatnia wartość rabatu (1%)
def test_apply_discount_one_percent():
    repo = FakeProductRepo()
    repo.save({
        "id": 1,
        "name": "Laptop",
        "price_net": 200.00,
        "price_gross": 246.00
    })

    service = ProductService(repo)

    updated = service.apply_discount(1, 1)

    assert updated["price_net"] == 198.00
    assert updated["price_gross"] == 243.54

# METODA NR 10 – test 3 => (przypadek brzegowy) maksymalna dozwolona wartość rabatu (89%)
def test_apply_discount_upper_limit():
    repo = FakeProductRepo()
    repo.save({
        "id": 1,
        "name": "Laptop",
        "price_net": 100.00,
        "price_gross": 123.00
    })

    service = ProductService(repo)

    updated = service.apply_discount(1, 89)

    assert updated["price_net"] == 11.00
    assert updated["price_gross"] == 13.53

# METODA NR 10 – test 4 => ValueError - rabat równy 0% jest niedozwolony
def test_apply_discount_zero_percent():
    repo = FakeProductRepo()
    service = ProductService(repo)

    with pytest.raises(ValueError):
        service.apply_discount(1, 0)

# METODA NR 10 – test 5 => ValueError - rabat mniejszy od zera
def test_apply_discount_negative_percent():
    repo = FakeProductRepo()
    service = ProductService(repo)

    with pytest.raises(ValueError):
        service.apply_discount(1, -5)

# METODA NR 10 – test 6 => ValueError - rabat równy 90% (przekroczenie górnej granicy)
def test_apply_discount_ninety_percent():
    repo = FakeProductRepo()
    service = ProductService(repo)

    with pytest.raises(ValueError):
        service.apply_discount(1, 90)


# METODA NR 10 – test 7 => ValueError - rabat większy niż 90%
def test_apply_discount_above_ninety_percent():
    repo = FakeProductRepo()
    service = ProductService(repo)

    with pytest.raises(ValueError):
        service.apply_discount(1, 100)


# METODA NR 10 – test 8 => ValueError - próba zastosowania rabatu do nieistniejącego produktu
def test_apply_discount_product_not_found():
    repo = FakeProductRepo()
    service = ProductService(repo)

    with pytest.raises(ValueError):
        service.apply_discount(1, 10)


# METODA NR 10 – test 9 => sprawdzenie poprawności zaokrągleń - cena po rabacie zostaje zaokrąglona do dwóch miejsc po przecinku
def test_apply_discount_rounding():
    repo = FakeProductRepo()
    repo.save({
        "id": 1,
        "name": "Phone",
        "price_net": 19.99,
        "price_gross": 24.59
    })

    service = ProductService(repo)

    updated = service.apply_discount(1, 10)

    assert updated["price_net"] == 17.99
    assert updated["price_gross"] == 22.13

# TESTY: METODA NR 11 - DELETE_PRODUCT

# METODA NR 11 – test 1 => happy path - poprawne usunięcie istniejącego produktu
def test_delete_product_success():
    repo = FakeProductRepo()
    repo.save({
        "id": 1,
        "name": "Laptop",
        "price_net": 100,
        "price_gross": 123
    })

    service = ProductService(repo)

    result = service.delete_product(1)

    assert result is True
    assert repo.get(1) is None


# METODA NR 11 – test 2 => produkt nie istnieje - metoda powinna zwrócić False
def test_delete_product_not_found():
    repo = FakeProductRepo()
    service = ProductService(repo)

    result = service.delete_product(1)

    assert result is False

# METODA NR 11 – test 3 => usunięcie jednego produktu - nie wpływa na pozostałe rekordy w repozytorium
def test_delete_product_does_not_remove_other_products():
    repo = FakeProductRepo()

    repo.save({"id": 1, "name": "A", "price_net": 10, "price_gross": 12.3})
    repo.save({"id": 2, "name": "B", "price_net": 20, "price_gross": 24.6})

    service = ProductService(repo)

    result = service.delete_product(1)

    assert result is True
    assert repo.get(1) is None
    assert repo.get(2) is not None

# METODA NR 11 – test 4 => ponowna próba usunięcia tego samego produktu - pierwsze usunięcie zwraca True, kolejne False
def test_delete_product_twice():
    repo = FakeProductRepo()

    repo.save({"id": 1, "name": "Laptop", "price_net": 100, "price_gross": 123})

    service = ProductService(repo)

    assert service.delete_product(1) is True
    assert service.delete_product(1) is False