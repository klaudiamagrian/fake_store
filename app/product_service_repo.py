import math


class ProductServiceRepo:
    """
    Serwis biznesowy do zarządzania produktami w bazie danych.
    """

    VAT_RATE = 0.23
    MAX_NAME_LENGTH = 80
    MAX_PRICE = 50000

    def __init__(self, repo):
        self.repo = repo

    # NORMALIZACJA -> METODA NR 1 - NORMALIZE_NAME

    def normalize_name(self, name: str) -> str:
        """Trim + usunięcie podwójnych spacji"""
        name = (name or "").strip()
        name = " ".join(name.split())
        return name

    # WALIDACJA -> METODA NR 2 - VALIDATE_NAME

    def validate_name(self, name: str) -> str:
        name = self.normalize_name(name)

        if len(name) < 3:
            raise ValueError("Product name too short")

        if len(name) > self.MAX_NAME_LENGTH:
            raise ValueError("Product name too long")

        return name

    # METODA NR 3 - VALIDATE_PRICE_NET

    def validate_price_net(self, price_net: float) -> float:
        if not isinstance(price_net, (int, float)):
            raise ValueError("Invalid net price type")

        if price_net <= 0:
            raise ValueError("Net price must be positive")

        if price_net > self.MAX_PRICE:
            raise ValueError("Net price too high")

        return round(float(price_net), 2)

    # METODA NR 4 - VALIDATE_PRICE_GROSS

    def validate_price_gross(self, price_net: float, price_gross: float) -> float:
        expected = price_net * (1 + self.VAT_RATE)

        if abs(price_gross - expected) > 0.05:
            raise ValueError("Gross price does not match VAT rate")

        return round(float(price_gross), 2)


    # OBLICZENIA: METODA NR 5 ORAZ METODA NR 6

    # METODA NR 5 - COMPUTE_GROSS_PRICE
    def compute_gross_price(self, price_net: float) -> float:
        """Oblicza cenę brutto na podstawie VAT"""
        return round(price_net * (1 + self.VAT_RATE), 2)

    # METODA NR 6 - COMPUTE_MARGIN
    def compute_margin(self, buy_price: float, sell_price: float) -> float:
        """Marża procentowa - o ile procent sprzedano drożej (albo taniej) niż kupiono"""
        if buy_price <= 0:
            raise ValueError("Invalid buy price")

        return round(((sell_price - buy_price) / buy_price) * 100, 2)

    # OPERACJE BIZNESOWE

    def create_product(self, product_id: int, name: str, price_net: float) -> int:
        """
        Tworzy produkt:
        - normalizuje nazwę
        - liczy cenę brutto
        - sprawdza istnienie w DB
        """

        name = self.validate_name(name)
        price_net = self.validate_price_net(price_net)
        price_gross = self.compute_gross_price(price_net)

        if self.repo.get(product_id):
            raise ValueError("Product already exists")

        self.repo.save(
            {
                "id": product_id,
                "name": name,
                "price_net": price_net,
                "price_gross": price_gross,
            }
        )

        return product_id

    def update_price(self, product_id: int, new_price_net: float):
        """
        Aktualizuje cenę produktu wraz z przeliczeniem VAT.
        """

        product = self.repo.get(product_id)
        if product is None:
            raise ValueError("Product not found")

        new_price_net = self.validate_price_net(new_price_net)
        new_price_gross = self.compute_gross_price(new_price_net)

        product["price_net"] = new_price_net
        product["price_gross"] = new_price_gross

        self.repo.update(product)

    def rename_product(self, product_id: int, new_name: str):
        """
        Zmiana nazwy produktu z walidacją.
        """

        product = self.repo.get(product_id)
        if product is None:
            raise ValueError("Product not found")

        new_name = self.validate_name(new_name)

        product["name"] = new_name
        self.repo.update(product)

    def apply_discount(self, product_id: int, percent: float):
        """
        Stosuje rabat procentowy.
        """

        if percent <= 0 or percent >= 90:
            raise ValueError("Invalid discount value")

        product = self.repo.get(product_id)
        if product is None:
            raise ValueError("Product not found")

        discounted = product["price_net"] * (1 - percent / 100)

        product["price_net"] = round(discounted, 2)
        product["price_gross"] = self.compute_gross_price(product["price_net"])

        self.repo.update(product)

    def delete_product(self, product_id: int) -> bool:
        """
        Usuwa produkt, jeśli istnieje.
        """

        if self.repo.get(product_id) is None:
            return False

        return self.repo.delete(product_id)
