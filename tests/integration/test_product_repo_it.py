import pytest
from app.product_repo import ProductRepo


# Pomocnicze: repo + czysta baza na start testu
@pytest.fixture
def repo():
    r = ProductRepo()
    r.ensure_schema()
    r.clear()
    return r


def assert_product_equal(db_row: dict, expected: dict):
    assert db_row["id"] == expected["id"]
    assert db_row["name"] == expected["name"]
    assert float(db_row["price_net"]) == float(expected["price_net"])
    assert float(db_row["price_gross"]) == float(expected["price_gross"])
    # external_id może nie być zwracany przez repo.get (u Ciebie SELECT nie wybiera external_id),
    # więc go tutaj nie sprawdzamy.


# ---------- CRUD (poprawione) ----------

def test_save_and_get_product(repo):
    product = {
        "external_id": None,
        "name": "Laptop",
        "price_net": 100.0,
        "price_gross": 123.0,
    }

    repo.save(product)
    # ID nadaje DB -> bierzemy z product["id"]
    result = repo.get(product["id"])
    assert result is not None
    assert_product_equal(result, product)


def test_get_when_product_not_exist(repo):
    assert repo.get(999999) is None


def test_update_existing_product(repo):
    product = {
        "external_id": None,
        "name": "Laptop",
        "price_net": 100.0,
        "price_gross": 123.0,
    }
    repo.save(product)

    updated = {
        "id": product["id"],
        "name": "Laptop Lenovo",
        "price_net": 200.0,
        "price_gross": 246.0,
    }

    ok = repo.update(updated)
    assert ok is True

    saved_product = repo.get(product["id"])
    assert saved_product["name"] == "Laptop Lenovo"
    assert float(saved_product["price_net"]) == 200.0
    assert float(saved_product["price_gross"]) == 246.0


def test_update_not_existing_product(repo):
    updated_product = {
        "id": 123456,
        "name": "Macbook",
        "price_net": 200.0,
        "price_gross": 246.0,
    }
    assert repo.update(updated_product) is False


def test_delete_existing_product(repo):
    product = {
        "external_id": None,
        "name": "Laptop",
        "price_net": 200.0,
        "price_gross": 246.0,
    }
    repo.save(product)

    ok = repo.delete(product["id"])
    assert ok is True
    assert repo.get(product["id"]) is None


@pytest.mark.parametrize("missing_id", [99, 9999, 123456])
def test_delete_not_existing_product(repo, missing_id):
    assert repo.delete(missing_id) is False


# ---------- Brakujące testy: get_all ----------

def test_get_all_returns_all_products(repo):
    p1 = {"external_id": None, "name": "Aaa", "price_net": 10.0, "price_gross": 12.3}
    p2 = {"external_id": None, "name": "Bbb", "price_net": 20.0, "price_gross": 24.6}
    repo.save(p1)
    repo.save(p2)

    all_products = repo.get_all()
    assert len(all_products) == 2

    ids = {row["id"] for row in all_products}
    assert p1["id"] in ids
    assert p2["id"] in ids


# ---------- Brakujące testy: external_id (integracja z importem z API) ----------

@pytest.mark.parametrize(
    "external_id, name, net",
    [
        (1, "API A", 10.0),
        (999, "API B", 20.0),
    ],
)
def test_get_by_external_id(repo, external_id, name, net):
    product = {
        "external_id": external_id,
        "name": name,
        "price_net": net,
        "price_gross": round(net * 1.23, 2),
    }
    repo.save(product)

    got = repo.get_by_external_id(external_id)
    assert got is not None
    assert got["external_id"] == external_id
    assert got["name"] == name


# ---------- Brakujące testy: price snapshot / historia ----------

def test_add_snapshot_and_get_price_history(repo):
    product = {"external_id": None, "name": "X", "price_net": 10.0, "price_gross": 12.3}
    repo.save(product)

    repo.add_price_snapshot(product["id"], 10.0, 12.3)
    repo.add_price_snapshot(product["id"], 8.0, 9.84)

    hist = repo.get_price_history(product["id"])
    assert len(hist) == 2
    assert float(hist[0]["price_net"]) == 10.0
    assert float(hist[1]["price_net"]) == 8.0


# ---------- Brakujące testy: best_deals ----------

def test_best_deals_orders_by_drop(repo):
    # produkt 1: spadek 2
    p1 = {"external_id": None, "name": "P1", "price_net": 10.0, "price_gross": 12.3}
    repo.save(p1)
    repo.add_price_snapshot(p1["id"], 10.0, 12.3)
    repo.add_price_snapshot(p1["id"], 8.0, 9.84)

    # produkt 2: spadek 5
    p2 = {"external_id": None, "name": "P2", "price_net": 20.0, "price_gross": 24.6}
    repo.save(p2)
    repo.add_price_snapshot(p2["id"], 20.0, 24.6)
    repo.add_price_snapshot(p2["id"], 15.0, 18.45)

    deals = repo.get_best_deals(limit=5)
    assert len(deals) >= 1
    assert deals[0]["name"] == "P2"
    assert float(deals[0]["drop_net"]) == 5.0


def test_best_deals_ignores_products_with_single_snapshot(repo):
    p = {"external_id": None, "name": "OnlyOne", "price_net": 10.0, "price_gross": 12.3}
    repo.save(p)
    repo.add_price_snapshot(p["id"], 10.0, 12.3)

    deals = repo.get_best_deals(limit=5)
    # HAVING samples >= 2 => nie powinno być w wynikach
    assert all(d["name"] != "OnlyOne" for d in deals)


# ---------- Brakujące testy: walidacja repo (negatywne przypadki) ----------

@pytest.mark.parametrize(
    "bad_product",
    [
        {"external_id": None, "name": "", "price_net": 10.0, "price_gross": 12.3},          # pusta nazwa
        {"external_id": None, "name": "   ", "price_net": 10.0, "price_gross": 12.3},       # same spacje
        {"external_id": None, "name": "X", "price_net": -1.0, "price_gross": 0.0},          # ujemna cena
        {"external_id": None, "name": "X", "price_net": 10.0, "price_gross": 9.0},          # gross < net
        {"external_id": None, "name": "X", "price_net": "10", "price_gross": 12.3},         # zły typ
    ],
)
def test_save_rejects_invalid_product(repo, bad_product):
    with pytest.raises(ValueError):
        repo.save(bad_product)