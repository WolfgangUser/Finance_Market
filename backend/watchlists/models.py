from django.db import models
from django.utils import timezone


class Watchlist(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='watchlists')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['user', 'name']

    def __str__(self):
        return f"{self.user.email} - {self.name}"


class WatchlistAsset(models.Model):
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE, related_name='assets')
    asset = models.ForeignKey('assets.Asset', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['watchlist', 'asset']

    def __str__(self):
        return f"{self.watchlist.name} - {self.asset.ticker}"
