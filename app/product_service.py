class ProductService:
    """
    GŁÓWNY SERWIS BIZNESOWY PRODUKTÓW

    - zawiera całą logikę biznesową
    - nie zna HTTP
    - nie zna FakeStore API
    - nie zna SQL
    - komunikuje się wyłącznie przez repozytorium
    """

    VAT_RATE = 0.23
    MAX_NAME_LENGTH = 80
    MAX_PRICE = 50_000

    def __init__(self, repo):
        self.repo = repo

    # =========================
    # NORMALIZACJA I WALIDACJA
    # =========================

    def normalize_name(self, name: str) -> str:
        name = (name or "").strip()
        return " ".join(name.split())

    def validate_name(self, name: str) -> str:
        name = self.normalize_name(name)

        if len(name) < 3:
            raise ValueError("Product name too short")

        if len(name) > self.MAX_NAME_LENGTH:
            raise ValueError("Product name too long")

        return name

    def validate_price_net(self, price_net: float) -> float:
        if not isinstance(price_net, (int, float)):
            raise ValueError("Invalid net price type")

        if price_net <= 0:
            raise ValueError("Net price must be positive")

        if price_net > self.MAX_PRICE:
            raise ValueError("Net price too high")

        return round(float(price_net), 2)

    # =========================
    # OBLICZENIA
    # =========================

    def compute_gross_price(self, price_net: float) -> float:
        return round(price_net * (1 + self.VAT_RATE), 2)

    def compute_margin(self, buy_price: float, sell_price: float) -> float:
        if buy_price <= 0:
            raise ValueError("Invalid buy price")

        return round(((sell_price - buy_price) / buy_price) * 100, 2)

    # =========================
    # OPERACJE BIZNESOWE
    # =========================

    def create_product(self, product_id: int, name: str, price_net: float) -> dict:
        """
        Tworzy nowy produkt w systemie:
        - waliduje dane
        - liczy VAT
        - sprawdza unikalność
        - zapisuje do bazy
        """

        name = self.validate_name(name)
        price_net = self.validate_price_net(price_net)
        price_gross = self.compute_gross_price(price_net)

        if self.repo.get(product_id):
            raise ValueError("Product already exists")

        product = {
            "id": product_id,
            "name": name,
            "price_net": price_net,
            "price_gross": price_gross,
        }

        self.repo.save(product)
        return product

    def update_price(self, product_id: int, new_price_net: float) -> dict:
        product = self.repo.get(product_id)
        if product is None:
            raise ValueError("Product not found")

        new_price_net = self.validate_price_net(new_price_net)
        product["price_net"] = new_price_net
        product["price_gross"] = self.compute_gross_price(new_price_net)

        self.repo.update(product)
        return product

    def rename_product(self, product_id: int, new_name: str) -> dict:
        product = self.repo.get(product_id)
        if product is None:
            raise ValueError("Product not found")

        product["name"] = self.validate_name(new_name)
        self.repo.update(product)
        return product

    def apply_discount(self, product_id: int, percent: float) -> dict:
        if percent <= 0 or percent >= 90:
            raise ValueError("Invalid discount value")

        product = self.repo.get(product_id)
        if product is None:
            raise ValueError("Product not found")

        discounted = product["price_net"] * (1 - percent / 100)

        product["price_net"] = round(discounted, 2)
        product["price_gross"] = self.compute_gross_price(product["price_net"])

        self.repo.update(product)
        return product

    def delete_product(self, product_id: int) -> bool:
        if self.repo.get(product_id) is None:
            return False

        return self.repo.delete(product_id)
