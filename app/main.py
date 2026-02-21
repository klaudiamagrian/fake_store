from product_client import ProductClient
from product_repo import ProductRepo
from product_service import ProductService

# Ten plik to warstwa CLI - Command Line Interface (interfejs użytkownika)
# Ta aplikacja jest obsługiwana przez terminal:
# - wyświetla menu w terminalu,
# - przyjmuje dane przez input(),
# - wypisuje wynik przez print().

# Ta aplikacja nie ma:
# - GUI,
# - przeglądarki,
# - REST API.

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
        print("1. Dodaj produkt ręcznie") #product_service -> metoda create_product
        print("2. Wyświetl wszystkie produkty z FakeStore API") #product_client -> metoda list_all
        print("3. Dodaj produkt z FakeStore API") #product_client -> get(product_id), później product_service -> create_product()
        print("4. Aktualizuj cenę produktu") #product_service -> update_price(), później product_repo -> get(), update(), add_price_snapshot()
        print("5. Zmień nazwę produktu") #product_service -> rename_product
        print("6. Zastosuj rabat") #product_service -> apply_discount
        print("7. Usuń produkt") #product_service -> delete_product, później product_repo -> delete()
        print("8. Wyświetl produkt z bazy") #product_repo -> get()
        print("9. Wyświetl wszystkie produkty z bazy") #product_repo -> get_all
        print("10. Ranking best deals (największy spadek ceny)") #product_service -> best_deals(), później product_repo -> get_best_deals
        print("0. Wyjście")


        choice = input("Wybierz opcję: ")

        try:
            if choice == "1":
                name = input("Nazwa produktu: ")
                price = input_float("Cena netto: ")
                product = service.create_product(name, price)
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
                product = service.create_product(
                    name=api_product["title"],
                    price_net=api_product["price"],
                    external_id=api_product["id"],
            )
                print("Dodano produkt z API:", product)

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

            elif choice == "10":
                limit = input_int("Ile pozycji rankingu: ")
                deals = service.best_deals(limit)
                for d in deals:
                    print(f"ID:{d['id']} {d['name']} drop_net={d['drop_net']} min={d['min_net']} max={d['max_net']} samples={d['samples']}")

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
