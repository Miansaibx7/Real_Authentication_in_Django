import os
import requests


class RapidAPIService:

    BASE_URL = "https://real-time-amazon-data.p.rapidapi.com"

    @staticmethod
    def get_products_by_category(country="US"):

        api_key = os.getenv("RAPIDAPI_KEY")

        url = f"{RapidAPIService.BASE_URL}/product-category-list"

        headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com",
        }

        params = {
            "country": country
        }

        response = requests.get(url, headers=headers, params=params, timeout=20)