import os
import pymysql


class ProductRepo:
    """Repozytorium DB do zarządzania produktami"""

    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.user = os.getenv("DB_USER", "root")
        self.db = os.getenv("DB_NAME", "store")

    def _conn(self):
        return pymysql.connect(
            host=self.host,
            user=self.user,
            database=self.db,
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor,
        )

    # ========= FIXTURE =========

    def ensure_schema(self):
        with self._conn() as c, c.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    id INT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    price_net FLOAT NOT NULL,
                    price_gross FLOAT NOT NULL
                )
                """
            )

    def clear(self):
        """Czyści tabelę – używane w testach integracyjnych"""
        with self._conn() as c, c.cursor() as cur:
            cur.execute("DELETE FROM products")

    # ========= CRUD =========

    def save(self, product: dict):
        with self._conn() as c, c.cursor() as cur:
            cur.execute(
                """
                INSERT INTO products (id, name, price_net, price_gross)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    product["id"],
                    product["name"],
                    product["price_net"],
                    product["price_gross"],
                ),
            )

    def get(self, product_id: int):
        with self._conn() as c, c.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, price_net, price_gross
                FROM products
                WHERE id=%s
                """,
                (product_id,),
            )
            return cur.fetchone()

    def update(self, product: dict) -> bool:
        with self._conn() as c, c.cursor() as cur:
            cur.execute(
                """
                UPDATE products
                SET name=%s,
                    price_net=%s,
                    price_gross=%s
                WHERE id=%s
                """,
                (
                    product["name"],
                    product["price_net"],
                    product["price_gross"],
                    product["id"],
                ),
            )
            return cur.rowcount > 0

    def delete(self, product_id: int) -> bool:
        with self._conn() as c, c.cursor() as cur:
            cur.execute(
                "DELETE FROM products WHERE id=%s",
                (product_id,),
            )
            return cur.rowcount > 0
