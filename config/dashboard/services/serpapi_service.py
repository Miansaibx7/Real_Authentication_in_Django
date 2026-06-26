import os
import requests


class TrendService:

    @staticmethod
    def get_trends(location="PK"):

        api_key = os.getenv("SERPAPI_API_KEY")

        url = "https://serpapi.com/search"

        params = {
            "engine": "google_trends_trending_now",
            "geo": location,
            "api_key": api_key
        }

        response = requests.get(url, params=params, timeout=20)

        if response.status_code != 200:
            return []

        data = response.json()

        return [
            {
                "query": item.get("query"),
                "trend_score": item.get("search_interest", 50)
            }
            for item in data.get("trending_searches", [])
        ]