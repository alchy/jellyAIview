import requests
from typing import Dict, List, Union
from datetime import datetime


class JellyAPI:
    """
    Třída pro komunikaci s Jelly vizualizační aplikací pomocí REST API.
    """

    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Inicializace API klienta.

        Args:
            base_url (str): Základní URL adresa API (výchozí: http://localhost:8000)
        """
        self.base_url = base_url.rstrip('/')

    def add_data(self, data: Dict[str, float]) -> Dict[str, str]:
        """
        Přidá nový objekt dat do vizualizace.

        Args:
            data (Dict[str, float]): Slovník obsahující páry klíč-hodnota pro vizualizaci

        Returns:
            Dict[str, str]: Odpověď serveru obsahující status a zprávu

        Raises:
            requests.exceptions.RequestException: Při chybě komunikace s API
            ValueError: Při neplatných datech
        """
        try:
            response = requests.post(
                f"{self.base_url}/data",
                json={"data": data}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Chyba při komunikaci s API: {str(e)}")
        except ValueError as e:
            raise ValueError(f"Neplatná data: {str(e)}")

    def get_data(self) -> List[Dict[str, float]]:
        """
        Získá všechna aktuální data z vizualizace.

        Returns:
            List[Dict[str, float]]: Seznam všech objektů dat

        Raises:
            requests.exceptions.RequestException: Při chybě komunikace s API
        """
        try:
            response = requests.get(f"{self.base_url}/data")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Chyba při komunikaci s API: {str(e)}")

    def clear_data(self) -> Dict[str, str]:
        """
        Vymaže všechna data z vizualizace.

        Returns:
            Dict[str, str]: Odpověď serveru obsahující status a zprávu

        Raises:
            requests.exceptions.RequestException: Při chybě komunikace s API
        """
        try:
            response = requests.delete(f"{self.base_url}/data")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Chyba při komunikaci s API: {str(e)}")
