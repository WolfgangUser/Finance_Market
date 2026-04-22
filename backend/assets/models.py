from django.db import models
from django.utils import timezone


class Asset(models.Model):
    ASSET_TYPES = [
        ('stock', 'Stock'),
        ('crypto', 'Crypto'),
        ('forex', 'Forex'),
    ]

    ticker = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=ASSET_TYPES)
    sector = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.ticker} - {self.name}"


class PriceData(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='prices')
    open = models.DecimalField(max_digits=15, decimal_places=4)
    close = models.DecimalField(max_digits=15, decimal_places=4)
    high = models.DecimalField(max_digits=15, decimal_places=4)
    low = models.DecimalField(max_digits=15, decimal_places=4)
    volume = models.DecimalField(max_digits=20, decimal_places=4)
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['asset', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.asset.ticker} - {self.timestamp}"
