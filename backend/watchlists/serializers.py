from rest_framework import serializers
from .models import Watchlist, WatchlistAsset


class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = ['id', 'user_id', 'name', 'created_at']
        read_only_fields = ['id', 'user_id', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class WatchlistAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchlistAsset
        fields = ['id', 'watchlist_id', 'asset_id']
        read_only_fields = ['id']
