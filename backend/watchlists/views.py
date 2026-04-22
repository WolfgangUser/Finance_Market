from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import Watchlist, WatchlistAsset
from .serializers import WatchlistSerializer, WatchlistAssetSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class WatchlistListCreateView(generics.ListCreateAPIView):
    serializer_class = WatchlistSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class WatchlistAddAssetView(generics.GenericAPIView):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistAssetSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def post(self, request, pk):
        watchlist = self.get_object()
        if watchlist.user != request.user:
            return Response({'error': 'You do not have permission to modify this watchlist'}, status=status.HTTP_403_FORBIDDEN)
        
        asset_id = request.data.get('asset_id')
        if not asset_id:
            return Response({'error': 'asset_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if asset exists
        from assets.models import Asset
        try:
            asset = Asset.objects.get(id=asset_id)
        except Asset.DoesNotExist:
            return Response({'error': 'Asset not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if already in watchlist
        if WatchlistAsset.objects.filter(watchlist=watchlist, asset=asset).exists():
            return Response({'error': 'Asset already in watchlist'}, status=status.HTTP_400_BAD_REQUEST)
        
        WatchlistAsset.objects.create(watchlist=watchlist, asset=asset)
        return Response({'message': 'Asset added successfully'}, status=status.HTTP_200_OK)


class WatchlistRemoveAssetView(generics.GenericAPIView):
    queryset = Watchlist.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def delete(self, request, pk):
        watchlist = self.get_object()
        if watchlist.user != request.user:
            return Response({'error': 'You do not have permission to modify this watchlist'}, status=status.HTTP_403_FORBIDDEN)
        
        asset_id = request.data.get('asset_id')
        if not asset_id:
            return Response({'error': 'asset_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        deleted_count, _ = WatchlistAsset.objects.filter(watchlist=watchlist, asset_id=asset_id).delete()
        if deleted_count == 0:
            return Response({'error': 'Asset not found in watchlist'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({'message': 'Asset removed successfully'}, status=status.HTTP_200_OK)
