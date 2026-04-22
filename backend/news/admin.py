from django.contrib import admin
from .models import MarketNews


@admin.register(MarketNews)
class MarketNewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'source', 'published_at', 'asset']
    list_filter = ['source', 'published_at']
    search_fields = ['title', 'content']
