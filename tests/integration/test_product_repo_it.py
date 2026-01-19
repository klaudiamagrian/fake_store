import pytest
from app.product_repo import ProductRepo


class TestProductRepositoryIntegration:

    # ========= SCHEMA (raz na sesję) =========
    @pytest.fixture(scope="session", autouse=True)
    def ensure_schema(self):
        repo = ProductRepo()
        repo.ensure_schema()

    # ========= RESET DB (przed KAŻDYM testem) =========
    @pytest.fixture(autouse=True)
    def reset_db(self):
        repo = ProductRepo()
        with repo._conn() as c, c.cursor() as cur:
            cur.execute("DELETE FROM products")
            cur.execute(
                """
                INSERT INTO products (id, name, price_net, price_gross)
                VALUES (%s, %s, %s, %s)
                """,
                (1, "BaseProduct", 10.0, 12.3),
            )

    # ========= HELPER =========
    def get_count(self) -> int:
        repo = ProductRepo()
        with repo._conn() as c, c.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS cnt FROM products")
            row = cur.fetchone()
            return row["cnt"]

    # ========= TESTY =========
    @pytest.mark.parametrize(
        "product",
        [
            {"id": 2, "name": "ProdA", "price_net": 20.0, "price_gross": 24.6},
            {"id": 3, "name": "ProdB", "price_net": 30.0, "price_gross": 36.9},
        ],
    )
    def test_add_product(self, product):
        repo = ProductRepo()
        repo.save(product)
        loaded = repo.get(product["id"])
        assert loaded["name"] == product["name"]

    @pytest.mark.parametrize(
        "product",
        [
            {"id": 4, "name": "ProdC", "price_net": 40.0, "price_gross": 49.2},
            {"id": 5, "name": "ProdD", "price_net": 50.0, "price_gross": 61.5},
        ],
    )
    def test_add_product_by_count(self, product):
        initial = self.get_count()
        repo = ProductRepo()
        repo.save(product)
        assert self.get_count() == initial + 1

    def test_get_all_products_by_count(self):
        initial = self.get_count()
        assert self.get_count() == initial

    @pytest.mark.parametrize(
        "product",
        [
            {"id": 6, "name": "ProdE", "price_net": 10.0, "price_gross": 12.3},
            {"id": 7, "name": "ProdF", "price_net": 15.0, "price_gross": 18.45},
        ],
    )
    def test_update_product(self, product):
        repo = ProductRepo()
        repo.save(product)

        updated = dict(product)
        updated["price_gross"] += 10

        repo.update(updated)
        result = repo.get(product["id"])

        assert result["price_gross"] == updated["price_gross"]

    @pytest.mark.parametrize(
        "product",
        [
            {"id": 8, "name": "ProdG", "price_net": 5.0, "price_gross": 6.15},
            {"id": 9, "name": "ProdH", "price_net": 8.0, "price_gross": 9.84},
        ],
    )
    def test_delete_product_by_count(self, product):
        repo = ProductRepo()
        initial = self.get_count()

        repo.save(product)
        repo.delete(product["id"])

        assert self.get_count() == initial
        assert repo.get(product["id"]) is None
