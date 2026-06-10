from django.db import models
from django.utils import timezone
from apps.core.models import TimeStampedModel


class PromotionStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    ACTIVE = "active", "Active"
    EXPIRED = "expired", "Expired"
    CANCELLED = "cancelled", "Cancelled"


class Promotion(TimeStampedModel):
    place = models.ForeignKey("places.Place", on_delete=models.PROTECT, related_name="promotions")
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="promotions",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=PromotionStatus.choices, default=PromotionStatus.DRAFT, db_index=True)

    class Meta:
        db_table = "promotions"
        ordering = ["-start_date"]
        indexes = [
            models.Index(fields=["status", "end_date"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.status})"

    @property
    def is_currently_active(self):
        now = timezone.now()
        return self.status == PromotionStatus.ACTIVE and self.start_date <= now <= self.end_date
