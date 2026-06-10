from django.db import models
from apps.core.models import TimeStampedModel


class EventStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    PUBLISHED = "published", "Published"
    CANCELLED = "cancelled", "Cancelled"
    FINISHED = "finished", "Finished"


class Event(TimeStampedModel):
    place = models.ForeignKey(
        "places.Place",
        on_delete=models.PROTECT,
        related_name="events",
        null=True,
        blank=True,
    )
    organizer = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="organized_events",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    category = models.CharField(max_length=100, db_index=True)
    start_date = models.DateTimeField(db_index=True)
    end_date = models.DateTimeField()
    minimum_age = models.PositiveSmallIntegerField(default=0)
    capacity = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image_url = models.URLField(blank=True, default="")
    status = models.CharField(max_length=20, choices=EventStatus.choices, default=EventStatus.DRAFT, db_index=True)
    cancellation_reason = models.TextField(blank=True, default="")

    class Meta:
        db_table = "events"
        ordering = ["start_date"]
        indexes = [
            models.Index(fields=["status", "start_date"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.status})"

    def can_publish(self):
        return self.status == EventStatus.DRAFT

    def can_cancel(self):
        return self.status == EventStatus.PUBLISHED

    def can_finish(self):
        return self.status == EventStatus.PUBLISHED
