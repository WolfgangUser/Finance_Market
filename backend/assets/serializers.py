from rest_framework import serializers
from .models import Asset, PriceData


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'ticker', 'name', 'type', 'sector', 'created_at']
        read_only_fields = ['id', 'created_at']


class PriceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceData
        fields = ['id', 'asset_id', 'open', 'close', 'high', 'low', 'volume', 'timestamp']
        read_only_fields = ['id']


class PriceDataListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceData
        fields = ['timestamp', 'close']
