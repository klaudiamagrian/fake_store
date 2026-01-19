# app/main.py
from product_client import ProductClient
from product_repo import ProductRepo
from product_service import ProductService

def main():
    client = ProductClient()
    repo = ProductRepo()
    repo.ensure_schema()
    service = ProductService(client, repo)

    print("=== Product Importer ===")
    pid = int(input("Podaj ID produktu (Fake Store API): "))

    try:
        product = service.fetch_and_store(pid)
        print("Zapisano produkt do bazy:")
        print(product)
    except Exception as e:
        print("Błąd:", e)

if __name__ == "__main__":
    main()

