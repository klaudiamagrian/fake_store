from product_client import ProductClient
from product_repo import ProductRepo
from product_service import ProductService

def input_int(prompt: str) -> int:
    """Bezpieczne wczytanie liczby całkowitej od użytkownika"""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Nieprawidłowa wartość. Podaj liczbę całkowitą.")

def input_float(prompt: str) -> float:
    """Bezpieczne wczytanie liczby zmiennoprzecinkowej od użytkownika"""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Nieprawidłowa wartość. Podaj liczbę.")

def main():
    client = ProductClient()
    repo = ProductRepo()
    repo.ensure_schema()
    service = ProductService(repo)

    while True:
        print("\n=== MENU ===")
        print("1. Dodaj produkt ręcznie")
        print("2. Wyświetl wszystkie produkty z FakeStore API")
        print("3. Dodaj produkt z FakeStore API")
        print("4. Aktualizuj cenę produktu")
        print("5. Zmień nazwę produktu")
        print("6. Zastosuj rabat")
        print("7. Usuń produkt")
        print("8. Wyświetl produkt z bazy")
        print("9. Wyświetl wszystkie produkty z bazy")
        print("0. Wyjście")

        choice = input("Wybierz opcję: ")

        try:
            if choice == "1":
                name = input("Nazwa produktu: ")
                price = input_float("Cena netto: ")
                product = service.create_product( name, price)
                print("Dodano produkt:", product)

            elif choice == "2":
                products = client.list_all()
                if products:
                    for p in products:
                        print(f"ID: {p['id']}, Nazwa: {p['title']}, Cena: {p['price']}")
                else:
                    print("Brak produktów w API")

            elif choice == "3":
                pid = input_int("ID produktu z API: ")
                try:
                    api_product = client.get(pid)
                except Exception as e:
                    print("Błąd pobrania produktu z API:", e)
                    continue
                try:
                    product = service.create_product(
                        name=api_product["title"],
                        price_net=api_product["price"]
                    )
                    print("Dodano produkt z API:", product)
                except ValueError as ve:
                    print("Błąd walidacji produktu:", ve)

            elif choice == "4":
                pid = input_int("ID produktu: ")
                new_price = input_float("Nowa cena netto: ")
                product = service.update_price(pid, new_price)
                print("Zaktualizowano cenę:", product)

            elif choice == "5":
                pid = input_int("ID produktu: ")
                new_name = input("Nowa nazwa produktu: ")
                product = service.rename_product(pid, new_name)
                print("Zmieniono nazwę:", product)

            elif choice == "6":
                pid = input_int("ID produktu: ")
                percent = input_float("Procent rabatu: ")
                product = service.apply_discount(pid, percent)
                print("Zastosowano rabat:", product)

            elif choice == "7":
                pid = input_int("ID produktu: ")
                result = service.delete_product(pid)
                print("Usunięto produkt" if result else "Produkt nie istnieje")

            elif choice == "8":
                pid = input_int("ID produktu: ")
                product = repo.get(pid)
                print(product if product else "Produkt nie istnieje")

            elif choice == "9":
                products = repo.get_all()
                for p in products:
                    print(f"ID: {p['id']}, Nazwa: {p['name']}, Cena netto: {p['price_net']}, Cena brutto: {p['price_gross']}")


            elif choice == "0":
                print("Koniec programu")
                break

            else:
                print("Niepoprawna opcja. Spróbuj ponownie.")

        except ValueError as ve:
            print("Błąd:", ve)
        except Exception as e:
            print("Nieoczekiwany błąd:", e)


if __name__ == "__main__":
    main()
