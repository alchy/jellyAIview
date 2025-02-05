from api.jellyAPI import JellyAPI
import time
from datetime import datetime
import random


def generate_sample_data() -> dict:
    """Generuje vzorek náhodných dat pro vizualizaci."""
    words = ['test', 'example', 'sample', 'data', 'value', 'item']
    data = {}

    # Generování 3-6 náhodných položek
    for _ in range(random.randint(3, 6)):
        key = random.choice(words)
        # Generování hodnoty mezi -1 a 1
        value = round(random.uniform(-1, 1), 2)
        data[key] = value

    return data


def main():
    # Vytvoření instance API klienta
    api = JellyAPI()

    try:
        # Získání aktuálních dat
        print("Aktuální data v aplikaci:")
        current_data = api.get_data()
        for i, data in enumerate(current_data):
            print(f"Objekt {i + 1}:", data)

        # Přidání nových dat
        print("\nPřidávání nových dat...")
        for i in range(3):
            new_data = generate_sample_data()
            print(f"\nPřidávám data {i + 1}:", new_data)

            response = api.add_data(new_data)
            print("Odpověď serveru:", response)

            # Krátká pauza pro lepší vizuální efekt
            time.sleep(2)

        # Zobrazení aktualizovaných dat
        print("\nAktualizovaná data v aplikaci:")
        updated_data = api.get_data()
        for i, data in enumerate(updated_data):
            print(f"Objekt {i + 1}:", data)

        # Ukázka vymazání dat (zakomentováno pro bezpečnost)
        # print("\nMažu všechna data...")
        # response = api.clear_data()
        # print("Odpověď serveru:", response)

    except ConnectionError as e:
        print(f"Chyba připojení: {e}")
    except Exception as e:
        print(f"Neočekávaná chyba: {e}")


if __name__ == "__main__":
    main()