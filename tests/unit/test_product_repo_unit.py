import pytest
from app.product_service_repo import ProductServiceRepo

# TESTY: METODA NR 1 - NORMALIZE_NAME

# METODA NR 1 - test 1 => happy path "Laptop" = "Laptop"
def test_normalize_name_happy_path():
    service = ProductServiceRepo(None)
    assert service.normalize_name("Laptop") == "Laptop"

# METODA NR 1 - test 2 => usuwanie nadmiarowych spacji z początku, środka i końca string
def test_normalize_name_delete_too_many_spaces():
    service = ProductServiceRepo(None)
    assert service.normalize_name("    Laptop    Apple    MacBook     ") == "Laptop Apple MacBook"

# METODA NR 1 - test 3 => zwrot pustego stringa, jeśli jest początkowo pusty
def test_normalize_name_empty_string():
    service = ProductServiceRepo(None)
    assert service.normalize_name("") == ""

# METODA NR 1 - test 4 => jeśli None => wynik = "" (pusty string)
def test_normalize_name_if_none_then_empty_string():
    service = ProductServiceRepo(None)
    assert service.normalize_name(None) == ""

# TESTY: METODA NR 2 - VALIDATE_NAME

# METODA NR 2 - test 1 => (przypadek brzegowy) najmniejszy dopuszczalny string (ilość znaków = 3) i sprawdzenie usuwania spacji z końca i początku stringa
def test_validate_name_min_length():
    service = ProductServiceRepo(None)
    assert service.validate_name("   Tel     ") == "Tel"

# METODA NR 2 - test 2 => ValueError -> gdy długość string < 3
def test_validate_name_min_length():
    service = ProductServiceRepo(None)
    with pytest.raises(ValueError):
        assert service.validate_name("La")

# METODA NR 2 - test 3 => ValueError, jeśli ilość większa niż MAX_NAME_LENGTH = 80
def test_validate_name_above_max_length():
    service = ProductServiceRepo(None)
    with pytest.raises(ValueError):
        assert service.validate_name("A" * 81)

# METODA NR 2 - test 4 => (przypadek brzegowy) nie daje ValueError, jeśli długość string = 80
def test_validate_name_string_has_max_length():
    service = ProductServiceRepo(None)
    assert service.validate_name("A" * 80) == "A" * 80

# METODA NR 2 - test 5 => ValueError, gdy string jest pusty
def test_validate_name_string_is_empty():
    service = ProductServiceRepo(None)
    with pytest.raises(ValueError):
        service.validate_name("")

# METODA NR 2 - test 6 => ValueError, gdy w stringu same spacje
def test_validate_name_string_has_only_spaces():
    service = ProductServiceRepo(None)
    with pytest.raises(ValueError):
        service.validate_name("       ")

# METODA NR 2 - test 7 => ValueError, gdy string = None
def test_validate_name_string_is_none():
    service = ProductServiceRepo(None)
    with pytest.raises(ValueError):
        service.validate_name(None)

# TESTY: METODA NR 3 - VALIDATE_PRICE_NET

# METODA NR 3 - test 1 => ValueError, jeśli price_net to string
def test_validate_price_net_is_string():
    service = ProductServiceRepo(None)
    with pytest.raises(ValueError):
        service.validate_price_net("123")

# METODA NR 3 - test 2 => ValueError, jeśli price_net = None
def test_validate_price_net_is_none():
    service = ProductServiceRepo(None)
    with pytest.raises(ValueError):
        service.validate_price_net(None)

# METODA NR 3 - test 3 => (przypadek brzegowy) ValueError, jeśli price_net = 0
def test_validate_price_net_is_zero():
    service = ProductServiceRepo(None)
    with pytest.raises(ValueError):
        service.validate_price_net(0)

# METODA NR 3 - test 4 => ValueError, jeśli price_net < 0
def test_validate_price_net_is_below_zero():
    service = ProductServiceRepo(None)
    with pytest.raises(ValueError):
        service.validate_price_net(-7)

# METODA NR 3 - test 5 => happy path - zaokrąglenie do 2 miejsc po przecinku
def test_validate_price_net_happy_path():
    service = ProductServiceRepo(None)
    price_net = service.validate_price_net(19.999)
    assert price_net == 20.00

# METODA NR 3 - test 6 => happy path - int zamiast float
def test_validate_price_is_int():
    service = ProductServiceRepo(None)
    price_net = service.validate_price_net(100)
    assert price_net == 100.00

# METODA NR 3 - test 7 => ValueError, jeśli price_net > MAX_PRICE = 50000
def test_validate_price_is_bigger_than_max_price():
    service = ProductServiceRepo(None)
    with pytest.raises(ValueError):
        service.validate_price_net(50001)

# METODA NR 3 - test 8 => (przypadek brzegowy) jeśli price_net = MAX_PRICE = 50000
def test_validate_price_is_max_price():
    service = ProductServiceRepo(None)
    price_net = service.validate_price_net(50000)
    assert price_net == 50000

# METODA NR 3 - test 9 => ValueError, jeśli price_net to lista (może być tylko int lub float)
def test_validate_price_is_list():
    service = ProductServiceRepo(None)
    with pytest.raises(ValueError):
        service.validate_price_net([1])

# TESTY: METODA NR 4 - VALIDATE_PRICE_GROSS

# METODA NR 4 - test 1 => happy path
def test_validate_price_gross():
    service = ProductServiceRepo(None)
    assert service.validate_price_gross(100, 123.00) == 123.00

# METODA NR 4 - test 2 => (przypadek brzegowy) sprawdza niższą tolerancję błędu obliczenia
def test_validate_price_gross_lower_tolerance():
    service = ProductServiceRepo(None)
    assert service.validate_price_gross(100, 122.95) == 122.95

# METODA NR 4 - test 3 => (przypadek brzegowy) sprawdza wyższą tolerancję błędu obliczenia
def test_validate_price_gross_upper_tolerance():
    service = ProductServiceRepo(None)
    assert service.validate_price_gross(100, 123.05) == 123.05

# METODA NR 4 - test 4 => sprawdza, czy zaokrągla do w miejsc po przecinku
def test_validate_price_gross_rounding():
    service = ProductServiceRepo(None)
    assert service.validate_price_gross(100, 123.049) == 123.05

# METODA NR 4 - test 5 => ValueError, jeśli poniżej tolerencji błędu
def test_validate_price_gross_below_mistake_tolerance():
    service = ProductServiceRepo(None)
    with pytest.raises(ValueError):
        service.validate_price_gross(100, 122.94)

# METODA NR 4 - test 6 => ValueError, jeśli powyżej tolerencji błędu
def test_validate_price_gross_under_mistake_tolerance():
    service = ProductServiceRepo(None)
    with pytest.raises(ValueError):
        service.validate_price_gross(100, 123.06)

# TESTY: METODA NR 5 - COMPUTE_GROSS_PRICE

# METODA NR 5 - test 1 => happy path
def test_compute_gross_price_happy_path():
    service = ProductServiceRepo(None)
    result = service.compute_gross_price(100)
    assert result == 123.00

# METODA NR 5 - test 2 => zaokrąglenie
def test_compute_gross_price_rounding():
    service = ProductServiceRepo(None)
    result = service.compute_gross_price(19.99) # gross_price = 19.99 * 1.23 = 24.5877
    assert result == 24.59

# METODA NR 5 - test 3 => price_net = 0
def test_compute_gross_price_is_zero():
    service = ProductServiceRepo(None)
    result = service.compute_gross_price(0)
    assert result == 0.00

# TESTY: METODA NR 6 - COMPUTE_MARGIN

# METODA NR 6 - test 1 =>