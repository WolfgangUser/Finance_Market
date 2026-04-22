from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import Asset, PriceData
from .serializers import AssetSerializer, PriceDataListSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_admin


class AssetListCreateView(generics.ListCreateAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Asset.objects.all()
        search = self.request.query_params.get('search', None)
        asset_type = self.request.query_params.get('type', None)
        
        if search:
            queryset = queryset.filter(ticker__icontains=search) | queryset.filter(name__icontains=search)
        if asset_type:
            queryset = queryset.filter(type=asset_type)
        
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AssetDetailView(generics.RetrieveAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class AssetPriceListView(generics.ListAPIView):
    serializer_class = PriceDataListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        asset_id = self.kwargs['asset_id']
        return PriceData.objects.filter(asset_id=asset_id).order_by('-timestamp')
