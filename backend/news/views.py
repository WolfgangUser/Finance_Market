from rest_framework import generics, permissions
from .models import MarketNews
from .serializers import MarketNewsSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_admin


class NewsListView(generics.ListAPIView):
    queryset = MarketNews.objects.all().order_by('-published_at')
    serializer_class = MarketNewsSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        asset_id = self.request.query_params.get('asset_id', None)
        if asset_id:
            queryset = queryset.filter(asset_id=asset_id)
        return queryset
