# Ten plik to logika biznesowa, czyli:
# - walidacja nazwy (min długość, max długość, normalizacja),
# - walidacja ceny (zakres, typ, max limit),
# - obliczanie VAT,
# - walidacja ceny brutto względem VAT,
# - limit ceny maksymalnej,
# - blokada duplikatu external_id,
# - historia cen (snapshot),
# - ranking best deals (SQL agregacyjny),
# - rabat z ograniczeniem 0–90%,
# - marża procentowa.

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

    # METODA NR 1 - NORMALIZE_NAME
    # usuwa spacje w nazwie produktu z początku, środka i końca tekstu
    def normalize_name(self, name: str) -> str:
        name = (name or "").strip()
        return " ".join(name.split())

    # METODA NR 2 - VALIDATE_NAME
    # - normalizacja wejścia (metoda 1),
    # - jeśli mniej niż 3 znaki w nazwie produktu -> ValueError
    # - jeśli więcej niż maksymalna długość (80) -> ValueError
    # - jeśli wszystko ok -> pewność, że nazwa jest znormalizowana oraz spełnia warunki długości
    def validate_name(self, name: str) -> str:
        name = self.normalize_name(name)
        if len(name) < 3:
            raise ValueError("Product name too short")
        if len(name) > self.MAX_NAME_LENGTH:
            raise ValueError("Product name too long")
        return name

    # METODA NR 3 - VALIDATE_PRICE_NET
    # sprawdza, czy:
    # - cena netto jest int lub float (walidacja typu danych) -> nie może być liczbą, [] - pustą tabelą lub None
    # - cena jest większa od zera (jeśli równa bądź mniejsza od zera = ValueError)
    # - cena nie przekracza maksymalnej ceny (50_000)
    # - następuje konwersja do typu danych float i zaokrąglenie do 2 miejsc po przecinku
    # - zwraca bezpieczną wartość do dalszego użycia
    def validate_price_net(self, price_net: float) -> float:
        if not isinstance(price_net, (int, float)):
            raise ValueError("Invalid net price type")
        if price_net <= 0:
            raise ValueError("Net price must be positive")
        if price_net > self.MAX_PRICE:
            raise ValueError("Net price too high")
        return round(float(price_net), 2)

    # METODA NR 4 - VALIDATE_PRICE_GROSS
    # - oblicza cenę brutto według wzoru,
    # -

    def validate_price_gross(self, price_net: float, price_gross: float) -> float:
        """
        Sprawdza czy cena brutto odpowiada cenie netto + VAT
        z tolerancją 5 groszy (błędy zaokrągleń).
        """

        expected = price_net * (1 + self.VAT_RATE)

        if abs(price_gross - expected) > 0.05: # abs => żeby nie miało znaczenia, czy różnica jest dodatnia czy ujemna
            raise ValueError("Gross price does not match VAT rate")

        return round(float(price_gross), 2)

    # OBLICZENIA

    # METODA NR 5 - COMPUTE_GROSS_PRICE

    def compute_gross_price(self, price_net: float) -> float:
        return round(price_net * (1 + self.VAT_RATE), 2)

    # METODA NR 6 - COMPUTE_MARGIN

    def compute_margin(self, buy_price: float, sell_price: float) -> float:
        if buy_price <= 0:
            raise ValueError("Invalid buy price")

        return round(((sell_price - buy_price) / buy_price) * 100, 2)


    # OPERACJE BIZNESOWE

    # METODA NR 7 - CREATE_PRODUCT


    def create_product(self, name: str, price_net: float, external_id: int | None = None) -> dict:
        name = self.validate_name(name)
        price_net = self.validate_price_net(price_net)
        price_gross = self.compute_gross_price(price_net)

        # jeśli produkt z API i external_id już istnieje -> nie duplikuj
        if external_id is not None:
            existing = self.repo.get_by_external_id(external_id)
            if existing:
                raise ValueError("Product with this external_id already exists")

        product = {
            "external_id": external_id,
            "name": name,
            "price_net": price_net,
            "price_gross": price_gross
        }
        self.repo.save(product)  # nada product["id"]

        # NOWOŚĆ: snapshot ceny przy utworzeniu
        self.repo.add_price_snapshot(product["id"], product["price_net"], product["price_gross"])
        return product


        # METODA NR 8 - UPDATE_PRICE

    def update_price(self, product_id: int, new_price_net: float) -> dict:
            product = self.repo.get(product_id)
            if product is None:
                raise ValueError("Product not found")
            new_price_net = self.validate_price_net(new_price_net)
            product["price_net"] = new_price_net
            product["price_gross"] = self.compute_gross_price(new_price_net)
            self.repo.update(product)
            self.repo.add_price_snapshot(product["id"], product["price_net"], product["price_gross"])
            return product


        # METODA NR 9 - RENAME_PRODUCT

    def rename_product(self, product_id: int, new_name: str) -> dict:
            product = self.repo.get(product_id)
            if product is None:
                raise ValueError("Product not found")

            product["name"] = self.validate_name(new_name)
            self.repo.update(product)
            return product

        # METODA NR 10 - APPLY_DISCOUNT

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
            self.repo.add_price_snapshot(product["id"], product["price_net"], product["price_gross"])
            return product


        # METODA NR 11 - DELETE_PRODUCT

    def delete_product(self, product_id: int) -> bool:
            if self.repo.get(product_id) is None:
                return False

            return self.repo.delete(product_id)

    def best_deals(self, limit: int = 5) -> list[dict]:
        if limit <= 0 or limit > 50:
            raise ValueError("Invalid limit")
        return self.repo.get_best_deals(limit)
