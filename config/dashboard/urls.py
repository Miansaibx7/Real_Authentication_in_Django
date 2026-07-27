
from django.urls import path

from .views import (TrendingProductsView,UserLocationView,DashboardView,
    ProductSearchView,ProductListCreateView,LocationListCreateView,
    SaleListCreateView
)

urlpatterns = [
    
    # Real-time trending + products endpoint 
    path('trending/', TrendingProductsView.as_view(), name='trending-products'),

    # IP-based location detection endpoint 
    path('user-location/', UserLocationView.as_view(), name='user-location'),

    # Main dashboard (aggregated AI system) endpoint 
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # search trends endpoint 
    path('search/', ProductSearchView.as_view(), name='product-search'),

    #  products list endpoint 
    path('products/', ProductListCreateView.as_view(), name='product-list'),

    #  locations endpoint 
    path('locations/', LocationListCreateView.as_view(), name='location-list'),

    # sales (future DATABASE) endpoint 
    path('sales/', SaleListCreateView.as_view(), name='sale-list'),
]