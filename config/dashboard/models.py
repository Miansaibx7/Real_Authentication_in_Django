from django.db import models


class Product(models.Model):
    keyword = models.CharField(max_length=255)
    trend_score = models.FloatField(default=0.0)
    search_volume = models.IntegerField(default=0)
    category = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, default="Global")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.keyword