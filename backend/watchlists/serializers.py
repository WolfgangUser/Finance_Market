from rest_framework import serializers
from .models import Watchlist, WatchlistAsset
from assets.models import Asset, PriceData


class AssetSummarySerializer(serializers.ModelSerializer):
    latest_price = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = ['id', 'ticker', 'name', 'type', 'sector', 'latest_price']

    def get_latest_price(self, obj):
        pd = PriceData.objects.filter(asset=obj).order_by('-timestamp').first()
        return str(pd.close) if pd else None


class WatchlistSerializer(serializers.ModelSerializer):
    assets = serializers.SerializerMethodField()

    class Meta:
        model = Watchlist
        fields = ['id', 'user_id', 'name', 'created_at', 'assets']
        read_only_fields = ['id', 'user_id', 'created_at', 'assets']

    def get_assets(self, obj):
        # Return list of asset summaries for the watchlist
        asset_links = WatchlistAsset.objects.filter(watchlist=obj).select_related('asset')
        assets = [link.asset for link in asset_links]
        return AssetSummarySerializer(assets, many=True).data


    def get_latest_price(self, asset):
        # helper if needed elsewhere
        pd = PriceData.objects.filter(asset=asset).order_by('-timestamp').first()
        return str(pd.close) if pd else None

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class WatchlistAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchlistAsset
        fields = ['id', 'watchlist_id', 'asset_id']
        read_only_fields = ['id']
