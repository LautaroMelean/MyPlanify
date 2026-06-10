import uuid
from django.db import models
from apps.core.models import SoftDeleteModel


class Place(SoftDeleteModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    category = models.CharField(max_length=100, db_index=True)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100, db_index=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    phone = models.CharField(max_length=50, blank=True, default="")
    website = models.URLField(blank=True, default="")
    image_url = models.URLField(blank=True, default="")
    price_level = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "places"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["city", "category"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.city})"
