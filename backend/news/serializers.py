from rest_framework import serializers
from .models import MarketNews


class MarketNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketNews
        fields = ['id', 'title', 'content', 'source', 'published_at', 'asset_id']
        read_only_fields = ['id', 'published_at']
