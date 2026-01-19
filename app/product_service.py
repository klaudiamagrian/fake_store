# app/product_service.py
class ProductService:
    """Logika biznesowa produktów"""

    def __init__(self, client, repo):
        self.client = client
        self.repo = repo

    def compute_gross_price(self, net_price: float) -> float:
        """Cena brutto = netto + 23% VAT"""
        if net_price <= 0:
            raise ValueError("Price must be positive")
        return round(net_price * 1.23, 2)

    def fetch_and_store(self, product_id: int) -> dict:
        """
        Pobiera produkt z API, liczy cenę brutto,
        zapisuje do DB i zwraca zapisany produkt
        """
        product = self.client.get(product_id)

        saved = {
            "id": product["id"],
            "name": product["title"],          # mapowanie z Fake Store API
            "price_net": product["price"],
            "price_gross": self.compute_gross_price(product["price"]),
        }

        self.repo.save(saved)
        return saved
