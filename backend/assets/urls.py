from django.urls import path
from .views import AssetListCreateView, AssetDetailView, AssetPriceListView

urlpatterns = [
    path('', AssetListCreateView.as_view(), name='asset-list'),
    path('<int:pk>/', AssetDetailView.as_view(), name='asset-detail'),
    path('<int:asset_id>/prices/', AssetPriceListView.as_view(), name='asset-prices'),
]
