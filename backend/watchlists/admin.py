from django.contrib import admin
from .models import Watchlist, WatchlistAsset


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created_at']
    list_filter = ['user']
    search_fields = ['name', 'user__email']


@admin.register(WatchlistAsset)
class WatchlistAssetAdmin(admin.ModelAdmin):
    list_display = ['watchlist', 'asset']
    list_filter = ['watchlist', 'asset']
