from django.db import models
from apps.core.models import SoftDeleteModel


class ActivityType(models.TextChoices):
    RESTAURANT = "restaurant", "Restaurant"
    BAR = "bar", "Bar"
    CINEMA = "cinema", "Cinema"
    MUSEUM = "museum", "Museum"
    PARK = "park", "Park"
    SPORTS = "sports", "Sports"
    CONCERT = "concert", "Concert"
    GAMING = "gaming", "Gaming"
    TOURISM = "tourism", "Tourism"
    SHOPPING = "shopping", "Shopping"


class Activity(SoftDeleteModel):
    place = models.ForeignKey(
        "places.Place",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activities",
    )
    city = models.CharField(max_length=100, blank=True, default="", db_index=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    category = models.CharField(max_length=100, db_index=True)
    activity_type = models.CharField(max_length=50, choices=ActivityType.choices, db_index=True)
    min_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_people = models.PositiveSmallIntegerField(default=1)
    max_people = models.PositiveSmallIntegerField(null=True, blank=True)
    indoor = models.BooleanField(default=False)
    outdoor = models.BooleanField(default=False)
    score_base = models.PositiveSmallIntegerField(default=50)

    class Meta:
        db_table = "activities"
        ordering = ["-score_base", "name"]
        indexes = [
            models.Index(fields=["activity_type", "is_active"]),
            models.Index(fields=["indoor", "outdoor"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.activity_type})"
