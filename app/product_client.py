# app/product_client.py
import requests

class ProductClient:
    """Klient HTTP do Fake Store API"""

    def __init__(self, base_url: str = "https://fakestoreapi.com/products"):
        self.base_url = base_url.rstrip("/")

    def get(self, product_id: int) -> dict:
        """Pobiera pojedynczy produkt po ID"""
        r = requests.get(f"{self.base_url}/{product_id}", timeout=5)
        r.raise_for_status()
        return r.json()

    def list_all(self) -> list[dict]:
        """Pobiera listę produktów"""
        r = requests.get(self.base_url, timeout=5)
        r.raise_for_status()
        return r.json()
