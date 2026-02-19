import os
from decimal import Decimal

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


    def ensure_schema(self):
        with self._conn() as c, c.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                     id INT PRIMARY KEY AUTO_INCREMENT,
                    external_id INT NULL,
                    name VARCHAR(255) NOT NULL,
                    price_net DECIMAL(10,2) NOT NULL,
                    price_gross DECIMAL(10,2) NOT NULL,
                    UNIQUE KEY uq_external_id (external_id)
                    )
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS product_prices (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    product_id INT NOT NULL,
                    price_net DECIMAL(10,2) NOT NULL,
                    price_gross DECIMAL(10,2) NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
                    )
                """
            )


    def clear(self):
        with self._conn() as c, c.cursor() as cur:
            cur.execute("DELETE FROM product_prices")
            cur.execute("DELETE FROM products")

    # ========= CRUD =========
    def validate_product(self, product: dict):
        if not isinstance(product.get("name"), str) or not product["name"].strip():
            raise ValueError("Product name must be a non-empty string")
    
        for key in ["price_net", "price_gross"]:
            if key not in product or not isinstance(product[key], (int, float, Decimal)) or product[key] < 0:
                raise ValueError(f"{key} must be a non-negative number")
    
        if product["price_gross"] < product["price_net"]:
            raise ValueError("price_gross cannot be lower than price_net")


    def save(self, product: dict):
        self.validate_product(product)
        with self._conn() as c, c.cursor() as cur:
            cur.execute(
                """
                INSERT INTO products (external_id, name, price_net, price_gross)
                VALUES (%s, %s, %s, %s)
                """,
                (product.get("external_id"), product["name"], product["price_net"], product["price_gross"])
            )
            product["id"] = cur.lastrowid


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

    def get_all(self):
        with self._conn() as c, c.cursor() as cur:
            cur.execute("SELECT * FROM products")
            return cur.fetchall()

    def update(self, product: dict) -> bool:
        self.validate_product(product)
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

    def add_price_snapshot(self, product_id: int, price_net: float, price_gross: float):
        with self._conn() as c, c.cursor() as cur:
            cur.execute(
                """
                INSERT INTO product_prices (product_id, price_net, price_gross)
                VALUES (%s, %s, %s)
                """,
                (product_id, price_net, price_gross),
            )

    def get_by_external_id(self, external_id: int):
        with self._conn() as c, c.cursor() as cur:
            cur.execute(
                "SELECT * FROM products WHERE external_id=%s",
                (external_id,),
            )
            return cur.fetchone()

    def get_price_history(self, product_id: int):
        with self._conn() as c, c.cursor() as cur:
            cur.execute(
                """
                SELECT price_net, price_gross, created_at
                FROM product_prices
                WHERE product_id=%s
                ORDER BY created_at ASC
                """,
                (product_id,),
            )
            return cur.fetchall()

    def get_best_deals(self, limit: int = 5):
        """
        Ranking produktów wg największego spadku ceny netto:
        (max_price - min_price) DESC
        """
        with self._conn() as c, c.cursor() as cur:
            cur.execute(
                """
                SELECT
                    p.id, p.name,
                    (MAX(pp.price_net) - MIN(pp.price_net)) AS drop_net,
                    MIN(pp.price_net) AS min_net,
                    MAX(pp.price_net) AS max_net,
                    COUNT(*) AS samples
                FROM products p
                         JOIN product_prices pp ON pp.product_id = p.id
                GROUP BY p.id, p.name
                HAVING samples >= 2
                ORDER BY drop_net DESC
                    LIMIT %s
                """,
                (limit,),
            )
            return cur.fetchall()
