from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import requests

from .services.serpapi_service import TrendService
from .services.aggregator_service import AggregatorService
from .services.demand_engine import DemandEngine
from .services.apify_service import ApifyService
from .services.rapidapi_service import RapidAPIService



# TREND + PRODUCT INTELLIGENCE
class TrendingProductsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        location = request.GET.get("location", "PK")
        trends = TrendService.get_trends(location)

        results = []
        for t in trends:
            # REAL products from Apify (NO MOCK)
            products = ApifyService.get_products(t["query"], location)

            for p in products:
                # optional enrichment
                enriched = RapidAPIService.enrich_product(p["title"])
                price = float(p.get("price")or enriched.get("price")or 50)
                rating = float(p.get("rating") or 3)

                demand_score = DemandEngine.calculate(t["trend_score"],price,rating)

                results.append({
                    "trend": t["query"],
                    "product": p["title"],
                    "price": price,
                    "rating": rating,
                    "source": p.get("source"),
                    "demand_score": demand_score
                })

        return Response({"location": location,"total_products": len(results),"products": results})



#  REAL USER LOCATION
class UserLocationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request:dict)-> dict:
        try:
            response = requests.get("http://ip-api.com/json/",timeout=5)

            data = response.json()
            return Response({"city": data.get("city"), "country": data.get("country"), "latitude": data.get("lat"),
                "longitude": data.get("lon")})

        except Exception as e:
            return Response({"error": str(e)},status=503)
        
        

# MAIN DASHBOARD (AGGREGATED)
class DashboardView(APIView):
    permission_classes = [AllowAny]

    def get(self, request:dict)-> dict:
        location = request.GET.get("location", "PK")
        data = AggregatorService.get_dashboard_data(location)

        return Response({"location": location, "total_products": len(data), "data": data })


# SEARCH TREND PRODUCTS
class ProductSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request:dict)-> dict:
        query = request.GET.get("query")
        if not query:
            return Response({"error": "query required"}, status=400)
        
        trends = TrendService.get_trends("PK")
        results = [t for t in trends if query.lower() in t["query"].lower()]

        return Response({"query": query, "results": results })



# PRODUCT LIST (REAL DATA)
class ProductListCreateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request:dict)-> dict:
        location = request.GET.get("location", "PK")
        trends = TrendService.get_trends(location)

        products = []
        for i, t in enumerate(trends):

            items = ApifyService.get_products(t["query"], location)
            for item in items:

                products.append({
                    "id": i + 1,
                    "name": item["title"],
                    "price": item.get("price"),
                    "rating": item.get("rating"),
                    "source": item.get("source"),
                    "trend": t["query"]
                })

        return Response(products)



#  STATIC LOCATIONS (CAN BE DB LATER)
class LocationListCreateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request:dict)-> dict:
        return Response([
            {"id": 1, "name": "Karachi", "country": "Pakistan"},
            {"id": 2, "name": "Lahore", "country": "Pakistan"},
            {"id": 3, "name": "Peshawar", "country": "Pakistan"},
        ])



# SALES (PLACEHOLDER - SHOULD BE DB)
class SaleListCreateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        return Response([
            {
                "id": 1,
                "product_name": "Sample Product",
                "location": "Karachi",
                "quantity": 100,
                "revenue": 5000,
                "sale_date": "2026-06-16"
            }
        ])