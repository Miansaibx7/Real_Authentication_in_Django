from .serpapi_service import TrendService
from .apify_service import ApifyService
from .rapidapi_service import RapidAPIService
from .demand_engine import DemandEngine


class AggregatorService:

    @staticmethod
    def get_dashboard_data(location):

        trends = TrendService.get_trends(location)

        final_data = []

        for t in trends:

            products = ApifyService.get_products(t["query"], location)

            for p in products:

                enriched = RapidAPIService.enrich_product(p["title"])

                price = float(p.get("price") or enriched.get("price") or 50)
                rating = float(p.get("rating") or 3)

                demand_score = DemandEngine.calculate(
                    t["trend_score"],
                    price,
                    rating
                )

                final_data.append({
                    "trend": t["query"],
                    "product": p["title"],
                    "price": price,
                    "rating": rating,
                    "source": p.get("source"),
                    "demand_score": demand_score
                })

        return final_data