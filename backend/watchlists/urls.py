from django.urls import path
from .views import WatchlistListCreateView, WatchlistAddAssetView, WatchlistRemoveAssetView

urlpatterns = [
    path('', WatchlistListCreateView.as_view(), name='watchlist-list'),
    path('<int:pk>/add/', WatchlistAddAssetView.as_view(), name='watchlist-add'),
    path('<int:pk>/remove/', WatchlistRemoveAssetView.as_view(), name='watchlist-remove'),
]
