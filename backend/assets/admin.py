from django.contrib import admin
from .models import Asset, PriceData


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['ticker', 'name', 'type', 'sector', 'created_at']
    list_filter = ['type']
    search_fields = ['ticker', 'name']


@admin.register(PriceData)
class PriceDataAdmin(admin.ModelAdmin):
    list_display = ['asset', 'open', 'close', 'high', 'low', 'volume', 'timestamp']
    list_filter = ['asset', 'timestamp']
