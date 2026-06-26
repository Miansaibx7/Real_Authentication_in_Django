import os
import requests


class ApifyService:

    @staticmethod
    def get_products(query, location="Pakistan"):

        token = os.getenv("APIFY_API_KEY")

        if not token:
            print("APIFY ERROR: Missing API Key")
            return []

        ACTOR_NAME = "burbn~google-shopping-scraper"

        url = (
            f"https://api.apify.com/v2/acts/{ACTOR_NAME}"
            f"/run-sync-get-dataset-items?token={token}"
        )

        payload = {
            "searchTerms": [query],
            "countryCode": "PK",
            "maxItems": 10
        }

        try:
            response = requests.post(
                url,
                json=payload,
                timeout=120
            )

            print("APIFY STATUS:", response.status_code)

            # 🚨 Handle API failure safely
            if response.status_code != 200:
                print("APIFY ERROR RESPONSE:", response.text[:500])
                return []

            try:
                data = response.json()
            except ValueError:
                print("APIFY ERROR: Invalid JSON response")
                return []

            products = []

            for item in data or []:
                products.append({
                    "title": item.get("title"),
                    "price": item.get("price"),
                    "rating": item.get("rating", 0),
                    "source": "Google Shopping"
                })

            return products

        except requests.exceptions.Timeout:
            print("APIFY ERROR: Request timed out")
            return []

        except requests.exceptions.ConnectionError:
            print("APIFY ERROR: Connection error (network issue)")
            return []

        except requests.exceptions.RequestException as e:
            print("APIFY ERROR:", str(e))
            return []

        except Exception as e:
            print("APIFY UNKNOWN ERROR:", str(e))
            return []