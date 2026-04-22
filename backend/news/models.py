from django.db import models
from django.utils import timezone


class MarketNews(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    source = models.CharField(max_length=255)
    published_at = models.DateTimeField(default=timezone.now)
    asset = models.ForeignKey('assets.Asset', on_delete=models.CASCADE, null=True, blank=True, related_name='news')

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title
