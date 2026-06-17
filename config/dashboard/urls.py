
from django.urls import path

from .views import (
    TrendingProductsView,
    UserLocationView,
    DashboardView,
    ProductSearchView,
    ProductListCreateView,
    LocationListCreateView,
    SaleListCreateView,
)

urlpatterns = [
    # 🔥 Real-time trending + products
    path('trending/', TrendingProductsView.as_view(), name='trending-products'),

    # 🌍 IP-based location detection
    path('user-location/', UserLocationView.as_view(), name='user-location'),

    # 📊 Main dashboard (aggregated AI system)
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # 🔍 search trends
    path('search/', ProductSearchView.as_view(), name='product-search'),

    # 📦 products list
    path('products/', ProductListCreateView.as_view(), name='product-list'),

    # 📍 locations
    path('locations/', LocationListCreateView.as_view(), name='location-list'),

    # 💰 sales (future DB)
    path('sales/', SaleListCreateView.as_view(), name='sale-list'),
]